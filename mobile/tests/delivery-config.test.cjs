const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const yaml=require('js-yaml');
const root=path.resolve(__dirname,'../..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');
test('prepared Render service is free, manual, one backend and no database provisioning',()=>{
 const config=yaml.load(read('render.yaml'));
 assert.equal(config.databases,undefined);assert.equal(config.services.length,1);
 const service=config.services[0];assert.equal(service.plan,'free');assert.equal(service.runtime,'python');
 assert.equal(service.autoDeployTrigger,'off');assert.equal(service.rootDir,'backend');
 assert.equal(service.startCommand,'python scripts/start.py');assert.equal(service.healthCheckPath,'/health');
 const variables=Object.fromEntries(service.envVars.map(item=>[item.key,item]));
 for(const name of ['DATABASE_URL','SUPABASE_SERVICE_ROLE_KEY','SUPABASE_URL']){assert.equal(variables[name].sync,false);assert.equal(variables[name].value,undefined);}
 assert.equal(variables.PYTHON_VERSION.value,read('backend/.python-version').trim());
 assert.ok(fs.existsSync(path.join(root,'backend',variables.DATABASE_SSL_ROOT_CERT.value)));
});
test('CI validates locally and never needs real project secrets or deploy jobs',()=>{
 const source=read('.github/workflows/validate.yml');const config=yaml.load(source);
 assert.deepEqual(Object.keys(config.jobs).sort(),['backend','mobile','postgres']);
 assert.equal(config.permissions.contents,'read');assert.equal(config.on.push,undefined);
 assert.equal(source.includes('${{ secrets.'),false);
 assert.match(source,/test_safe.py --integration/);assert.match(source,/npm run typecheck/);
 const steps=config.jobs.postgres.steps;
 const url=new URL(steps.find(step=>step.env?.FUGA_TEST_DATABASE_URL).env.FUGA_TEST_DATABASE_URL);
 assert.equal(url.hostname,'127.0.0.1');
 for(const job of Object.values(config.jobs)){assert.ok(job['timeout-minutes']<=15);assert.equal(job.environment,undefined);}
});
