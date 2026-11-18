export type WindowInsetsMetrics = {
 systemTop:number;systemBottom:number;systemLeft:number;systemRight:number;
 imeBottom:number;keyboardVisible:boolean;frameTop:number;frameLeft:number;
 viewportWidth:number;viewportHeight:number;windowWidth:number;windowHeight:number;
};
export type PublicInsets={top:number;bottom:number;left:number;right:number;keyboardVisible:boolean;ready:boolean};
export const emptyPublicInsets:PublicInsets={top:0,bottom:0,left:0,right:0,keyboardVisible:false,ready:false};

/** All values are dp from the current window, never a model-specific status/nav height. */
export function calculatePublicInsets(value:WindowInsetsMetrics):PublicInsets|null{
 if(!value||typeof value.keyboardVisible!=='boolean')return null;
 for(const key of ['systemTop','systemBottom','systemLeft','systemRight','imeBottom','frameTop','frameLeft','viewportWidth','viewportHeight','windowWidth','windowHeight'] as const){
  const number=value[key];
  if(typeof number!=='number'||!Number.isFinite(number)||number<0)return null;
 }
 if(!(value.viewportWidth>0&&value.viewportHeight>0&&value.windowWidth>0&&value.windowHeight>0))return null;
 const bottomObstruction=value.keyboardVisible?Math.max(value.systemBottom,value.imeBottom):value.systemBottom;
 return {
  top:Math.min(value.viewportHeight,Math.max(0,value.systemTop-value.frameTop)),
  bottom:Math.min(value.viewportHeight,Math.max(0,value.frameTop+value.viewportHeight-(value.windowHeight-bottomObstruction))),
  left:Math.min(value.viewportWidth,Math.max(0,value.systemLeft-value.frameLeft)),
  right:Math.min(value.viewportWidth,Math.max(0,value.frameLeft+value.viewportWidth-(value.windowWidth-value.systemRight))),
  keyboardVisible:value.keyboardVisible,ready:true,
 };
}
