const {validateBuildEnvironment}=require('./scripts/check-public-env.cjs');
const withReleaseSigning=require('./plugins/withReleaseSigning.cjs');
module.exports=({config})=>{
 validateBuildEnvironment(process.env);
 return withReleaseSigning(config);
};
