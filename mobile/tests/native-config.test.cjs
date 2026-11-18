const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const {withAndroidImagePickerPermissions}=require('expo-image-picker/plugin/build/withImagePicker');

test('image picker preserves the voice microphone and blocks the camera in Android manifest',async()=>{
 const original=JSON.parse(readFileSync(require.resolve('../app.json'),'utf8')).expo;
 const options=original.plugins.find(p=>Array.isArray(p)&&p[0]==='expo-image-picker')[1];
 const config=withAndroidImagePickerPermissions(structuredClone(original),options);
 const input={...config,modResults:{manifest:{$:{},'uses-permission':[{$:{'android:name':'android.permission.RECORD_AUDIO'}}]}},modRequest:{platform:'android',modName:'manifest',introspect:true},mods:{},_internal:{}};
 const evaluated=await config.mods.android.manifest(input);
 const permissions=evaluated.modResults.manifest['uses-permission'];
 const microphone=permissions.find(p=>p.$['android:name']==='android.permission.RECORD_AUDIO');
 assert.ok(microphone);
 assert.notEqual(microphone.$['tools:node'],'remove');
 assert.equal(permissions.find(p=>p.$['android:name']==='android.permission.CAMERA').$['tools:node'],'remove');
 assert.equal(original.scheme,'fugaplus');
});
