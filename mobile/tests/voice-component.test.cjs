const {test}=require('node:test');
const assert=require('node:assert/strict');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;
const turn=()=>new Promise(resolve=>setImmediate(resolve));
const button=renderer=>renderer.root.findAllByType('Pressable').find(node=>['Dictar gasto','Detener y transcribir'].includes(node.props.accessibilityLabel));
function voice(native,permission='granted'){
 return loadComponent('src/voice/VoiceInput.tsx',{
  'react-native':{Platform:{OS:'android'},PermissionsAndroid:{PERMISSIONS:{RECORD_AUDIO:'microphone'},RESULTS:{GRANTED:'granted'},request:async()=>permission}},
  'expo-modules-core':{requireOptionalNativeModule:()=>native},
 }).VoiceInput;
}
test('real VoiceInput preserves the written alternative when its native module is absent',async()=>{
 let renderer;const Component=voice(null);
 await act(async()=>{renderer=create(React.createElement(Component,{onTranscript:()=>assert.fail('No transcription expected')}));});
 assert.match(JSON.stringify(renderer.toJSON()),/Puedes escribir tu gasto/);
 assert.equal(button(renderer),undefined);
 await act(async()=>renderer.unmount());
});
test('real VoiceInput does not start recognition after microphone denial',async()=>{
 let renderer,starts=0;const Component=voice({start:async()=>{starts++;return '';},cancel:async()=>{}},'denied');
 await act(async()=>{renderer=create(React.createElement(Component,{onTranscript:()=>assert.fail('No transcription expected')}));});
 await act(async()=>{button(renderer).props.onPress();await turn();});
 assert.equal(starts,0);assert.match(JSON.stringify(renderer.toJSON()),/Sin permiso de micrófono/);
 await act(async()=>renderer.unmount());
});
test('real VoiceInput stops recognition, bounds the editable transcript and cancels on unmount',async()=>{
 let renderer,resolve,stops=0,cancels=0;const transcripts=[];
 const Component=voice({start:()=>new Promise(done=>resolve=done),stop:async()=>{stops++;resolve('  '+ 'a'.repeat(300)+'  ');},cancel:async()=>{cancels++;}});
 await act(async()=>{renderer=create(React.createElement(Component,{onTranscript:text=>transcripts.push(text)}));});
 await act(async()=>{button(renderer).props.onPress();await turn();});
 assert.equal(button(renderer).props.accessibilityLabel,'Detener y transcribir');assert.equal(transcripts.length,0);
 await act(async()=>{button(renderer).props.onPress();await turn();});
 assert.equal(stops,1);assert.deepEqual(transcripts,['a'.repeat(280)]);
 assert.equal(button(renderer).props.accessibilityLabel,'Dictar gasto');
 await act(async()=>renderer.unmount());assert.equal(cancels,1);
});
