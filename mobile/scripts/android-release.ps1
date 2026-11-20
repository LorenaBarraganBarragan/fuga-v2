param([ValidateSet('Check','Prepare','Apk')][string]$Task='Check')
$ErrorActionPreference='Stop'
$releaseLauncher=Join-Path $PSScriptRoot 'android-release.cjs'
$oldStore=[Environment]::GetEnvironmentVariable('FUGA_ANDROID_STORE_PASSWORD','Process')
$oldKey=[Environment]::GetEnvironmentVariable('FUGA_ANDROID_KEY_PASSWORD','Process')
function Convert-ReleaseSecret([Security.SecureString]$Value){
 $releasePointer=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
 try {return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($releasePointer)}
 finally {[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($releasePointer)}
}
try {
 if($Task -eq 'Apk'){
  # No passwords in source, arguments, transcripts, dotenv or persistent environment.
  if(-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '../../.tools/android-release-signing/fugaplus-release.keystore'))){
   throw 'Primero crea tu keystore privado siguiendo mobile/docs/APK_RELEASE_LOCAL.md.'
  }
  $storeSecret=Read-Host 'Contrasena del keystore release (solo en este equipo)' -AsSecureString
  if($storeSecret.Length -eq 0){throw 'La contrasena del keystore no puede estar vacia.'}
  $keySecret=Read-Host 'Contrasena de la clave; Enter si es la misma del keystore' -AsSecureString
  $env:FUGA_ANDROID_STORE_PASSWORD=Convert-ReleaseSecret $storeSecret
  $env:FUGA_ANDROID_KEY_PASSWORD=if($keySecret.Length){Convert-ReleaseSecret $keySecret}else{$env:FUGA_ANDROID_STORE_PASSWORD}
 }
 $releaseAction=if($Task -eq 'Apk'){'build'}else{$Task.ToLowerInvariant()}
 & node $releaseLauncher $releaseAction
 if($LASTEXITCODE -ne 0){throw 'La preparacion o compilacion release no termino. No compartas las contrasenas.'}
} finally {
 [Environment]::SetEnvironmentVariable('FUGA_ANDROID_STORE_PASSWORD',$oldStore,'Process')
 [Environment]::SetEnvironmentVariable('FUGA_ANDROID_KEY_PASSWORD',$oldKey,'Process')
 if($storeSecret){$storeSecret.Dispose()}
 if($keySecret){$keySecret.Dispose()}
}
