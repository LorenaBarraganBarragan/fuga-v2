import React from 'react';
import {requireNativeViewManager} from 'expo-modules-core';
import type {ViewProps} from 'react-native';
import type {WindowInsetsProbeProps} from './WindowInsetsProbe';
const NativeProbe:React.ComponentType<ViewProps&WindowInsetsProbeProps>=requireNativeViewManager('FugaWindowInsets');
export function WindowInsetsProbe(props:WindowInsetsProbeProps){
 return <NativeProbe {...props} style={{position:'absolute',top:0,left:0,width:1,height:1}} pointerEvents="none" accessible={false} importantForAccessibility="no-hide-descendants"/>;
}
