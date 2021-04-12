/*失敗頁面倒數讀秒*/
var num=10;
function reciprocal(){
    var reciprocal=document.getElementById("reciprocal");
    if(num>0){
        num=num-1;
        reciprocal.value=num;
        setTimeout("reciprocal()",1000);
    }
}