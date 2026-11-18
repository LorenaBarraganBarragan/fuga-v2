export function expenseError(amount:string,description:string,date:string,category:string,categoryIds:string[],today:string):string {
 if(!/^\d+$/.test(amount)||Number(amount)<1||Number(amount)>100000000)return 'Monto: utiliza un entero entre 1 y 100.000.000 COP.';
 if(!description.trim()||description.trim().length>120)return 'Descripción: utiliza de 1 a 120 caracteres.';
 if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||Number.isNaN(Date.parse(date))||new Date(date+'T12:00:00Z').toISOString().slice(0,10)!==date||date<'2020-01-01'||date>today)return 'Fecha: utiliza YYYY-MM-DD desde 2020 hasta hoy.';
 if(!categoryIds.includes(category))return 'Categoría: selecciona una del catálogo.';
 return '';
}
export function mayNotify(last:number,now:Date):boolean {
 const hour=Number(new Intl.DateTimeFormat('en-US',{timeZone:'America/Bogota',hour:'numeric',hourCycle:'h23'}).format(now));
 return hour>=8&&hour<21&&now.getTime()-last>=7*24*60*60*1000;
}
