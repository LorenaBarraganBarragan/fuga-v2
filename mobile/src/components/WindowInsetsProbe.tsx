import type {WindowInsetsMetrics} from '../lib/publicInsets';
export type WindowInsetsProbeProps={viewportWidth:number;viewportHeight:number;onInsetsChange:(event:{nativeEvent:WindowInsetsMetrics})=>void};
// Web/iOS retain their current safe-area handling; the Android resolver uses the native observer.
export function WindowInsetsProbe(_props:WindowInsetsProbeProps){return null;}
