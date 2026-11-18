const {validateBuildEnvironment}=require('./scripts/check-public-env.cjs');
module.exports=({config})=>{
 validateBuildEnvironment(process.env);
 return config;
};
