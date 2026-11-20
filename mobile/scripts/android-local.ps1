param([ValidateSet('Preflight','Debug','Apk','Manifest')][string]$Task='Preflight', [ValidatePattern('^[D-Z]$')][string]$BuildDrive='Q', [string]$MobileRoot='', [switch]$SkipPrebuild)
$ErrorActionPreference='Stop'
if($Task -eq 'Apk' -and $env:FUGA_RELEASE_PREPARED -ne '1'){
 throw 'Para release usa mobile/scripts/android-release.ps1 -Task Apk; carga solo variables publicas y exige firma propia.'
}
$mobileTaskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$repositoryTaskRoot=[IO.Path]::GetFullPath((Join-Path $mobileTaskRoot '..'))
$shortTaskRoot=$BuildDrive+':\'
$createdTaskMapping=$false
if(Test-Path -LiteralPath $shortTaskRoot){
 $sameTaskDirectory=node -e "const fs=require('node:fs');const a=fs.statSync(process.argv[1]),b=fs.statSync(process.argv[2]);process.stdout.write(String(a.ino===b.ino&&a.dev===b.dev));" $shortTaskRoot $repositoryTaskRoot
 if($sameTaskDirectory -ne 'true'){throw 'La unidad de compilacion esta ocupada por otra carpeta; elige otra letra con -BuildDrive.'}
}else{
 subst ($BuildDrive+':') $repositoryTaskRoot
 if($LASTEXITCODE -ne 0){throw 'No se pudo crear la ruta corta de compilacion.'}
 $createdTaskMapping=$true
}
$enteredTaskLocation=$false
try {
$repositoryTaskRoot=$shortTaskRoot
$mobileTaskRoot=Join-Path $repositoryTaskRoot 'mobile'
if($MobileRoot){
 $mobileTaskRoot=[IO.Path]::GetFullPath($MobileRoot)
 $packageTaskPath=Join-Path $mobileTaskRoot 'package.json'
 if(-not (Test-Path -LiteralPath $packageTaskPath) -or (Get-Content -Raw -LiteralPath $packageTaskPath | ConvertFrom-Json).name -ne 'fuga-plus-mobile'){throw 'MobileRoot debe apuntar a una copia preparada de FUGA+.'}
 Write-Output 'Proyecto de compilacion aislado seleccionado; herramientas del workspace original.'
}
$sdkTaskRoot=if($env:ANDROID_HOME){$env:ANDROID_HOME}else{Join-Path $repositoryTaskRoot '.tools\android-sdk'}
$sdkTaskManager=Join-Path $sdkTaskRoot 'cmdline-tools\latest\bin\sdkmanager.bat'
$adbTaskExecutable=Join-Path $sdkTaskRoot 'platform-tools\adb.exe'
if(-not (Test-Path -LiteralPath $sdkTaskManager)){throw 'Android SDK no disponible. Consulta mobile/docs/ANDROID_LOCAL.md.'}
$localTaskJdk=Join-Path $repositoryTaskRoot '.tools\jdk17'
if(Test-Path -LiteralPath (Join-Path $localTaskJdk 'bin\javac.exe')){$env:JAVA_HOME=$localTaskJdk}
if(-not $env:JAVA_HOME -or -not (Test-Path -LiteralPath (Join-Path $env:JAVA_HOME 'bin\javac.exe'))){throw 'JDK 17 no disponible. Define JAVA_HOME o prepara .tools/jdk17.'}
$javaTaskVersion=& (Join-Path $env:JAVA_HOME 'bin\java.exe') --version
if($LASTEXITCODE -ne 0 -or ($javaTaskVersion -join ' ') -notmatch '(?:openjdk|java) 17\.') {throw 'La toolchain requiere JDK 17. Revisa JAVA_HOME sin cambiar Java del sistema.'}
Write-Output 'JDK 17 validado.'
$ninjaTaskExecutable=Join-Path $sdkTaskRoot 'cmake\3.22.1\bin\ninja.exe'
if(Test-Path -LiteralPath $ninjaTaskExecutable){
 $ninjaTaskVersion=(& $ninjaTaskExecutable --version).Trim()
 if([version]$ninjaTaskVersion -lt [version]'1.12.0'){Write-Warning 'Ninja antiguo: las rutas largas pueden bloquear CMake. Consulta ANDROID_LOCAL.md.'}
 else{Write-Output ('Ninja '+$ninjaTaskVersion+' localizado.')}
}
$env:ANDROID_HOME=$sdkTaskRoot
$env:ANDROID_SDK_ROOT=$sdkTaskRoot
$env:GRADLE_USER_HOME=Join-Path $repositoryTaskRoot '.tools\gradle'
# Builds from this script never read .env.local. Supply public values explicitly in this process.
$env:EXPO_NO_DOTENV='1'
$env:FUGA_RELEASE_BUILD=if($Task -eq 'Apk'){'1'}else{'0'}
$env:CI='1'
$env:DEBUG=''
Push-Location $mobileTaskRoot
$enteredTaskLocation=$true
 node scripts/check-public-env.cjs
 if($LASTEXITCODE -ne 0){throw 'Configuracion publica no valida.'}
 if($Task -in @('Debug','Manifest') -and (Test-Path -LiteralPath $adbTaskExecutable)){
  $deviceTaskLines=& $adbTaskExecutable devices
  foreach($deviceTaskLine in $deviceTaskLines){if($deviceTaskLine -match '\s+(device|unauthorized|offline)$'){Write-Output ('Android: '+$Matches[1])}}
 }
 if($Task -eq 'Preflight'){Write-Output 'SDK localizado; verificar plataforma, build-tools, NDK y telefono antes de compilar.';return}
 if(-not $SkipPrebuild){
  node node_modules/expo/bin/cli prebuild --platform android --no-install
  if($LASTEXITCODE -ne 0){throw 'Expo prebuild fallo.'}
 }elseif(-not (Test-Path -LiteralPath (Join-Path $mobileTaskRoot 'android\gradlew.bat'))){throw 'SkipPrebuild requiere un proyecto Android ya generado y vigente.'}
 Push-Location android
 try {
  $gradleTask=if($Task -eq 'Debug'){'assembleDebug'}elseif($Task -eq 'Manifest'){'processDebugMainManifest'}else{'assembleRelease'}
  # SUBST and canonical C: sources have different roots for Kotlin's incremental cache.
  & .\gradlew.bat $gradleTask --no-daemon --max-workers=4 '-PreactNativeArchitectures=arm64-v8a' '-Pkotlin.incremental=false' '-Pkotlin.compiler.execution.strategy=in-process' '-Dorg.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=1024m -Dfile.encoding=UTF-8' '-Djava.net.preferIPv4Stack=true' '-Dorg.gradle.internal.http.connectionTimeout=30000' '-Dorg.gradle.internal.http.socketTimeout=60000'
  if($LASTEXITCODE -ne 0){throw 'La compilacion Android no termino correctamente.'}
 } finally {Pop-Location}
} finally {
 if($enteredTaskLocation){Pop-Location}
 if($createdTaskMapping){subst ($BuildDrive+':') /d}
}
