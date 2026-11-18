/** Compile real TSX for Node tests; only native host controls and providers are simulated. */
const fs=require('node:fs');
const path=require('node:path');
const Module=require('node:module');
const ts=require('typescript');
const React=require('react');
const TestRenderer=require('react-test-renderer');
globalThis.IS_REACT_ACT_ENVIRONMENT=true;

function loadComponent(relative,overrides={}){
 const root=path.resolve(__dirname,'..'),cache=new Map();
 const native={Platform:{OS:'web'},Text:'Text',View:'View',TextInput:'TextInput',Pressable:'Pressable',ScrollView:'ScrollView',Modal:'Modal',ActivityIndicator:'ActivityIndicator',Image:'Image',StyleSheet:{create:x=>x},...overrides['react-native']};
 function load(filename){
  if(cache.has(filename))return cache.get(filename).exports;
  const module=new Module(filename);cache.set(filename,module);module.filename=filename;module.paths=Module._nodeModulePaths(path.dirname(filename));
  const original=module.require.bind(module);
  module.require=request=>{
   if(request==='react-native')return native;
   if(Object.hasOwn(overrides,request))return overrides[request];
   if(request.startsWith('.')){
    const target=path.resolve(path.dirname(filename),request);
    if(Object.hasOwn(overrides,target))return overrides[target];
    if(fs.existsSync(target+'.tsx'))return load(target+'.tsx');
    if(fs.existsSync(target+'.ts'))return original(target+'.ts');
   }
   return original(request);
  };
  const compiled=ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true}});
  module._compile(compiled.outputText,filename);return module.exports;
 }
 return load(path.resolve(root,relative));
}
module.exports={React,TestRenderer,loadComponent};
