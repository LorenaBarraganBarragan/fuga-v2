/** Persistent native signing configuration. Reads credentials only in Gradle, never in JS. */
const {withAppBuildGradle}=require('expo/config-plugins');
const BEGIN='// FUGA RELEASE SIGNING BEGIN',END='// FUGA RELEASE SIGNING END';
const signing=`${BEGIN}
def fugaSigning = [
    store: System.getenv('FUGA_ANDROID_KEYSTORE_PATH'),
    alias: System.getenv('FUGA_ANDROID_KEY_ALIAS'),
    storePassword: System.getenv('FUGA_ANDROID_STORE_PASSWORD'),
    keyPassword: System.getenv('FUGA_ANDROID_KEY_PASSWORD')
]
android {
    signingConfigs {
        fugaRelease {
            if (fugaSigning.store) storeFile file(fugaSigning.store)
            if (fugaSigning.alias) keyAlias fugaSigning.alias
            if (fugaSigning.storePassword) storePassword fugaSigning.storePassword
            if (fugaSigning.keyPassword) keyPassword fugaSigning.keyPassword
        }
    }
}
gradle.taskGraph.whenReady { graph ->
    if (graph.allTasks.any { it.project.path == ':app' && it.name.contains('Release') }) {
        if (fugaSigning.values().any { !it } || !file(fugaSigning.store).isFile()) {
            throw new GradleException('Firma release incompleta. Usa el lanzador android-release.ps1 con tu keystore privado.')
        }
        if (file(fugaSigning.store).canonicalFile == file('debug.keystore').canonicalFile) {
            throw new GradleException('La firma release no puede utilizar debug.keystore.')
        }
    }
}
${END}
`;

function applyReleaseSigning(source){
 let text=source.replace(new RegExp(BEGIN+'[\\s\\S]*?'+END+'(?:\\r?\\n){0,2}','g'),'');
 const build=text.indexOf('buildTypes {'),start=text.indexOf('release {',build);
 if(build<0||start<0)throw new Error('No se encontró el bloque Android release esperado.');
 // Only change the signing line of release, keeping debug and every other setting.
 const tail=text.slice(start),match=/signingConfig\s+signingConfigs\.(debug|fugaRelease)\b/.exec(tail);
 if(!match)throw new Error('La firma release existente no es la plantilla esperada; revisa antes de reemplazarla.');
 const prefix=tail.slice('release {'.length,match.index).replace(/\/\/[^\n]*(?:\n|$)/g,'').trim();
 if(prefix)throw new Error('El bloque release tiene una estructura no reconocida; no se cambia su firma.');
 const index=start+match.index;
 text=text.slice(0,index)+'signingConfig signingConfigs.fugaRelease'+text.slice(index+match[0].length);
 const android=/^android\s*\{/m.exec(text);
 if(!android)throw new Error('No se encontró la configuración Android.');
 return text.slice(0,android.index)+signing+'\n'+text.slice(android.index);
}
function withReleaseSigning(config){
 return withAppBuildGradle(config,result=>{
  if(result.modResults.language!=='groovy')throw new Error('La firma FUGA+ requiere el proyecto Gradle Groovy existente.');
  result.modResults.contents=applyReleaseSigning(result.modResults.contents);return result;
 });
}
module.exports=withReleaseSigning;
module.exports.applyReleaseSigning=applyReleaseSigning;
