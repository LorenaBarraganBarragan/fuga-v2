const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {validatePhotoAsset,photoUploadForm,photoUploadFailure,appendNativePhoto}=require('../src/lib/profilePhoto.ts');
const {act,create}=TestRenderer;
const file=name=>path.resolve(__dirname,'../src',name);
const button=(renderer,title)=>renderer.root.findAllByType('Pressable').find(n=>n.props.accessibilityLabel===title);
const selected={uri:'file:///local-fixture.png',fileName:'fixture.png',mimeType:'image/png',fileSize:100};
const signature={timestamp:1,public_id:'fuga/local-fixture/asset',signature:'temporary-signature',api_key:'public-upload-key',upload_url:'https://api.cloudinary.com/local-fixture/image/upload',overwrite:'false',allowed_formats:'jpg,jpeg,png,webp'};
signature.upload_url='https://api.cloudinary.com/v1_1/local-fixture/image/upload';

function screen({asset=selected,permission=true,canceled=false,api=async()=>{},auth:customAuth}={}){
 const calls=[];
 const auth=customAuth||{session:{user:{id:'fixture-user'}},profile:{rol:'usuario',foto_url:'https://old.example.test/photo.png'},reload:async()=>{},logout:async()=>{}};
 const {Profile}=loadComponent('src/screens/Profile.tsx',{
  [file('auth/AuthProvider')]:{useAuth:()=>auth},
  [file('lib/api')]:{api:async(route,options)=>{calls.push({route,options});return route==='/me/photo/signature'?signature:api(route,options);}},
  'react-native':{Platform:{OS:'android'}},
  'expo-file-system':{File:class FixtureFile extends Blob{constructor(){super([new Uint8Array(100)],{type:'image/png'});this.name='fixture.png';}async bytes(){return new Uint8Array(await this.arrayBuffer());}}},
  'expo-image-picker':{requestMediaLibraryPermissionsAsync:async()=>({granted:permission}),launchImageLibraryAsync:async()=>({canceled,assets:[asset]})},
 });
 return {Profile,calls,auth};
}

test('photo validation accepts boundary JPEG/PNG/WebP and rejects unknown size or unsupported files',()=>{
 for(const mimeType of ['image/jpeg','image/png','image/webp'])assert.equal(validatePhotoAsset({...selected,mimeType,fileSize:5_000_000}).fileSize,5_000_000);
 for(const change of [{mimeType:'image/gif'},{mimeType:undefined},{fileSize:undefined},{fileSize:0},{fileSize:NaN},{fileSize:5_000_001}])assert.throws(()=>validatePhotoAsset({...selected,...change}));
});

test('native photo uses a File accepted by the actual installed Expo 58 multipart converter',async()=>{
 const fs=require('node:fs'),Module=require('node:module'),ts=require('typescript');
 function compile(name,overrides={}){
  const filename=path.resolve(__dirname,'../node_modules/expo/src',name),module=new Module(filename);
  const original=module.require.bind(module);module.require=name=>Object.hasOwn(overrides,name)?overrides[name]:original(name);
  module._compile(ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
  return module.exports;
 }
 const utils=compile('utils/blobUtils.ts');
 const {convertFormDataAsync}=compile('winter/fetch/convertFormData.ts',{'../../utils/blobUtils':utils});
 await assert.rejects(()=>convertFormDataAsync({entries:()=>[['file',{uri:'file:///fixture.png',name:'fixture.png',type:'image/png'}]]},'qa-boundary'),/Unsupported FormDataPart/);
 const image=fs.readFileSync(path.resolve(__dirname,'fixtures/profile-qa-a.png'));
 const nativeFile={name:'fixture.png',type:'image/png',size:image.length,bytes:async()=>new Uint8Array(image)};
 let captured;
 appendNativePhoto({append:(name,value)=>{assert.equal(name,'file');captured=value;}},selected,()=>nativeFile);
 assert.equal(captured,nativeFile);assert.equal(captured.uri,undefined);
 const result=await convertFormDataAsync({entries:()=>[['file',captured]]},'qa-boundary');
 assert.ok(Buffer.from(result.body).includes(image));
 assert.match(Buffer.from(result.body).toString('latin1'),/filename="fixture.png"/);
 assert.throws(()=>appendNativePhoto({append(){}},selected,()=>({...nativeFile,size:5_000_001})),/5 MB/);
});

test('upload form sends only signed fields to the fixed HTTPS Cloudinary endpoint',()=>{
 const form=photoUploadForm({...signature,CLOUDINARY_API_SECRET:'never-send'});
 assert.equal(form.get('CLOUDINARY_API_SECRET'),null);assert.equal(form.get('overwrite'),'false');
 for(const url of ['http://api.cloudinary.com/v1_1/a/image/upload','https://evil.invalid/upload','https://api.cloudinary.com.evil.invalid/v1_1/a/image/upload','https://private@api.cloudinary.com/v1_1/a/image/upload'])assert.throws(()=>photoUploadForm({...signature,upload_url:url}));
});

test('provider errors expose only safe classifications and HTTP status, never raw diagnostics',async()=>{
 for(const [status,message,expected] of [[400,'Invalid Signature PRIVATE_DETAIL',/firma/],[400,'Invalid image file PRIVATE_DETAIL',/formato/],[401,'PRIVATE_DETAIL',/autorizó/],[413,'PRIVATE_DETAIL',/tamaño/],[503,'PRIVATE_DETAIL',/disponible/],[400,'Stale request PRIVATE_DETAIL',/fecha/],[400,'PRIVATE_DETAIL',/rechazó/]]){
  const safe=await photoUploadFailure({status,json:async()=>({error:{message}})});
  assert.match(safe,expected);assert.match(safe,new RegExp('HTTP '+status));assert.doesNotMatch(safe,/PRIVATE_DETAIL/);
 }
 const safe=await photoUploadFailure({status:502,json:async()=>{throw new Error('PRIVATE_DETAIL');}});
 assert.match(safe,/HTTP 502/);assert.doesNotMatch(safe,/PRIVATE_DETAIL/);
});

test('Profile selection previews without signing or uploading; explicit cancellation preserves old photo',async()=>{
 const {Profile,calls}=screen();let renderer;
 await act(async()=>{renderer=create(React.createElement(Profile));});
 await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
 assert.equal(calls.length,0);
 assert.ok(button(renderer,'Confirmar fotografía').props.disabled);
 assert.equal(renderer.root.findAllByType('Image').length,2);
 await act(async()=>button(renderer,'Cancelar fotografía').props.onPress());
 assert.equal(calls.length,0);
 assert.equal(renderer.root.findAllByType('Image')[0].props.source.uri,'https://old.example.test/photo.png');
 await act(async()=>renderer.unmount());
});

test('Profile denied permission, picker cancellation and invalid files never sign an upload',async()=>{
 for(const options of [{permission:false},{canceled:true},{asset:{...selected,fileSize:5_000_001}},{asset:{...selected,mimeType:'image/gif'}}]){
  const {Profile,calls}=screen(options);let renderer;
  await act(async()=>{renderer=create(React.createElement(Profile));});
  await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
  assert.equal(calls.length,0);assert.equal(button(renderer,'Confirmar fotografía'),undefined);
  await act(async()=>renderer.unmount());
 }
});

test('Profile corrupt preview cannot be confirmed',async()=>{
 const {Profile,calls}=screen();let renderer;
 await act(async()=>{renderer=create(React.createElement(Profile));});
 await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
 const preview=renderer.root.findAllByType('Image').find(n=>n.props.accessibilityLabel.startsWith('Vista previa'));
 await act(async()=>preview.props.onError());
 assert.ok(button(renderer,'Confirmar fotografía').props.disabled);assert.equal(calls.length,0);
 assert.match(JSON.stringify(renderer.toJSON()),/No se pudo abrir/);
 await act(async()=>renderer.unmount());
});

test('Profile retries lost completion without reuploading and reloads the persisted photo',async t=>{
 let completions=0,uploads=0,reloads=0,renderer;
 t.mock.method(globalThis,'fetch',async()=>{uploads++;return {ok:true};});
 const {Profile,calls,auth}=screen({api:async route=>{if(route.endsWith('/complete')&&++completions===1)throw new Error('Respuesta perdida');}});
 auth.reload=async()=>{reloads++;};
 await act(async()=>{renderer=create(React.createElement(Profile));});
 await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
 await act(async()=>renderer.root.findAllByType('Image')[1].props.onLoad());
 await act(async()=>button(renderer,'Confirmar fotografía').props.onPress());
 assert.equal(uploads,1);assert.equal(completions,1);assert.equal(reloads,0);
 await act(async()=>button(renderer,'Confirmar fotografía').props.onPress());
 assert.equal(uploads,1);assert.equal(completions,2);assert.equal(reloads,1);
 assert.equal(calls.filter(c=>c.route.endsWith('/signature')).length,1);
 assert.match(JSON.stringify(renderer.toJSON()),/Fotografía actualizada/);
 await act(async()=>renderer.unmount());
});

test('Profile provider failure is generic and cancel registers the abandoned attempt',async t=>{
 t.mock.method(globalThis,'fetch',async()=>{throw new Error('PRIVATE_PROVIDER_DETAIL');});
 const {Profile,calls}=screen();let renderer;
 await act(async()=>{renderer=create(React.createElement(Profile));});
 await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
 await act(async()=>renderer.root.findAllByType('Image')[1].props.onLoad());
 await act(async()=>button(renderer,'Confirmar fotografía').props.onPress());
 assert.doesNotMatch(JSON.stringify(renderer.toJSON()),/PRIVATE_PROVIDER_DETAIL/);
 assert.match(JSON.stringify(renderer.toJSON()),/No se pudo cargar/);
 assert.equal(calls.filter(c=>c.route.endsWith('/complete')).length,0);
 await act(async()=>button(renderer,'Cancelar fotografía').props.onPress());
 assert.equal(calls.at(-1).route,'/me/photo/cancel');
 await act(async()=>renderer.unmount());
});

test('Profile unmount during provider upload never completes under another session',async t=>{
 let finish,renderer;
 t.mock.method(globalThis,'fetch',()=>new Promise(resolve=>{finish=resolve;}));
 const {Profile,calls}=screen();
 await act(async()=>{renderer=create(React.createElement(Profile));});
 await act(async()=>button(renderer,'Cambiar fotografía').props.onPress());
 await act(async()=>renderer.root.findAllByType('Image')[1].props.onLoad());
 let operation;
 await act(async()=>{operation=button(renderer,'Confirmar fotografía').props.onPress();await new Promise(resolve=>setImmediate(resolve));});
 await act(async()=>renderer.unmount());
 await act(async()=>{finish({ok:true});await operation;await new Promise(resolve=>setImmediate(resolve));});
 assert.equal(calls.filter(c=>c.route.endsWith('/complete')).length,0);
});
