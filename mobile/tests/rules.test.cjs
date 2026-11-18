const {test}=require('node:test');
const assert=require('node:assert/strict');
const {expenseError,mayNotify}=require('../src/lib/validation.ts');
const valid=['8000','Taxi','2026-11-15','cat',['cat'],'2026-11-15'];
test('gasto corregido válido y categoría del catálogo',()=>assert.equal(expenseError(...valid),''));
for(const amount of ['0','-1','8.5','8,50','100000001','NaN','1e3']){
 test('rechaza monto '+amount,()=>assert.match(expenseError(amount,...valid.slice(1)),/Monto/));
}
test('rechaza fechas inexistentes sin normalizarlas silenciosamente',()=>assert.match(expenseError('8000','Taxi','2026-02-30','cat',['cat'],'2026-11-15'),/Fecha/));
test('rechaza fechas futuras',()=>assert.match(expenseError('8000','Taxi','2026-11-16','cat',['cat'],'2026-11-15'),/Fecha/));
test('rechaza categorías ajenas al catálogo',()=>assert.match(expenseError('8000','Taxi','2026-11-15','otra',['cat'],'2026-11-15'),/Categoría/));
test('rechaza descripción vacía',()=>assert.match(expenseError('8000',' ','2026-11-15','cat',['cat'],'2026-11-15'),/Descripción/));
test('recordatorio permitido a las 08:00 Bogotá',()=>assert.equal(mayNotify(0,new Date('2026-11-15T13:00:00Z')),true));
test('silencio desde las 21:00 Bogotá',()=>assert.equal(mayNotify(0,new Date('2026-11-16T02:00:00Z')),false));
test('silencio antes de las 08:00 Bogotá',()=>assert.equal(mayNotify(0,new Date('2026-11-15T12:59:00Z')),false));
test('sin duplicar candidato en siete días',()=>{
 const now=new Date('2026-11-15T18:00:00Z');
 assert.equal(mayNotify(now.getTime()-6*86400000,now),false);
 assert.equal(mayNotify(now.getTime()-7*86400000,now),true);
});
