const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;

test('real Admin screen searches, filters and opens a fixture; state mutation requires explicit confirmation',async()=>{
 const calls=[];
 const account={id:'fictional-local-user',nombres:'Persona ficticia',apellido:'QA',email:'fixture@admin-qa.invalid',rol:'usuario',disabled_at:null,created_at:'2026-01-01',auth_sync_pendiente:false};
 const api=async(endpoint,options)=>{
  calls.push({endpoint,options});
  if(options?.method==='PATCH'){account.disabled_at=options.body.activo?null:'2026-01-01';return {auth_sincronizado:true};}
  if(endpoint.startsWith('/admin/users?'))return {items:[{...account}],has_more:false};
  if(endpoint==='/admin/stats')return {registrados:1,activos:1,inactivos:0,actividad_mensual:[{periodo:'2026-01-01',usuarios_activos:1}]};
  if(endpoint==='/admin/users/'+account.id)return {...account};
  throw new Error('Unexpected test route');
 };
 const {Admin}=loadComponent('src/screens/Admin.tsx',{[path.resolve(__dirname,'../src/lib/api')]:{api}});
 let renderer;await act(async()=>{renderer=create(React.createElement(Admin));});
 const button=label=>renderer.root.findAllByType('Pressable').find(n=>n.props.accessibilityLabel===label);
 await act(async()=>renderer.root.findByType('TextInput').props.onChangeText('fixture'));
 await act(async()=>button('Activas').props.onPress());
 await act(async()=>button('Buscar / actualizar').props.onPress());
 const request=calls.filter(c=>c.endpoint.startsWith('/admin/users?')).at(-1);
 const query=new URLSearchParams(request.endpoint.split('?')[1]);assert.equal(query.get('q'),'fixture');assert.equal(query.get('activo'),'true');
 await act(async()=>button('Ver cuenta').props.onPress());
 assert.ok(button('Volver al listado'));
 await act(async()=>button('Desactivar cuenta').props.onPress());
 assert.equal(calls.filter(c=>c.options?.method==='PATCH').length,0);
 const dialog=renderer.root.findByType('Modal');assert.equal(dialog.props.visible,true);
 await act(async()=>button('Confirmar').props.onPress());
 const mutations=calls.filter(c=>c.options?.method==='PATCH');assert.equal(mutations.length,1);
 assert.deepEqual(mutations[0],{endpoint:'/admin/users/'+account.id+'/state',options:{method:'PATCH',body:{activo:false}}});
 assert.ok(button('Buscar / actualizar'));
 await act(async()=>renderer.unmount());
});
