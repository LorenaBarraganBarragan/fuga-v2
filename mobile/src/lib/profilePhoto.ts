/** HU-08: fail closed when the picker cannot establish file type or size. */
export const MAX_PHOTO_BYTES=5_000_000;
export type PhotoSelection={uri:string;fileName?:string|null;mimeType?:string;fileSize?:number;file?:{size:number;type:string}};
export function validatePhotoAsset(asset:PhotoSelection){
 const size=asset.file?.size??asset.fileSize;
 const type=(asset.file?.type||asset.mimeType||'').toLowerCase();
 if(!['image/jpeg','image/png','image/webp'].includes(type))throw new Error('Selecciona una imagen JPEG, PNG o WebP.');
 if(typeof size!=='number'||!Number.isFinite(size)||size<=0)throw new Error('No se pudo verificar el tamaño de la fotografía. Selecciona otra imagen.');
 if(size>MAX_PHOTO_BYTES)throw new Error('La fotografía debe tener máximo 5 MB.');
 return {...asset,mimeType:type,fileSize:size};
}
export type PhotoSignature={timestamp:number;public_id:string;signature:string;api_key:string;upload_url:string;overwrite:string;allowed_formats:string};
export function appendNativePhoto(form:FormData,asset:PhotoSelection,createFile:(uri:string)=>{size:number;type:string;bytes:()=>Promise<Uint8Array>}){
 const file=createFile(asset.uri);
 validatePhotoAsset({...asset,file:{size:file.size,type:file.type||asset.mimeType||''}});
 // Expo 58 fetch serializes File/Blob values, not the legacy RN {uri,name,type} object.
 form.append('file',file as unknown as Blob);
}
export function photoUploadForm(signature:PhotoSignature){
 const url=new URL(signature.upload_url);
 if(url.protocol!=='https:'||url.hostname!=='api.cloudinary.com'||url.username||url.password||url.port||url.search||url.hash||!/^\/v1_1\/[a-zA-Z0-9_-]+\/image\/upload$/.test(url.pathname))throw new Error('Destino de fotografía no válido.');
 const form=new FormData();
 for(const name of ['api_key','timestamp','public_id','signature','overwrite','allowed_formats'] as const)form.append(name,String(signature[name]));
 return form;
}

export async function photoUploadFailure(response:{status:number;json:()=>Promise<unknown>}){
 let detail='';
 try{const value=await response.json() as {error?:{message?:unknown}};if(typeof value?.error?.message==='string')detail=value.error.message.toLowerCase();}catch{/* Never expose the provider response. */}
 const status=Number.isInteger(response.status)&&response.status>=100&&response.status<=599?response.status:0;
 let message='El almacenamiento rechazó la carga de la fotografía.';
 if(/signature/.test(detail))message='El almacenamiento rechazó la firma de carga. Revisa la configuración del servidor.';
 else if(/timestamp|stale request/.test(detail))message='El almacenamiento rechazó la fecha de la firma. Revisa el reloj del servidor.';
 else if(/format|invalid image/.test(detail))message='El almacenamiento rechazó el formato o contenido de la imagen.';
 else if(status===401||status===403)message='El almacenamiento no autorizó la carga. Revisa la configuración del servidor.';
 else if(status===413)message='La fotografía supera el tamaño admitido por el almacenamiento.';
 else if(status>=500)message='El almacenamiento no está disponible. Intenta más tarde.';
 return `${message} (HTTP ${status}).`;
}
