to_render = "I&-we&+am&";
console.log("hello");
l = to_render.length;
prev = -1;
final = '';
for(i=0; i<l; i++){
	next_string = '';
	if(to_render[i]=='&'){
		if(to_render[prev+1] =='+'){
			next_string = '<font color="red">' + '<del>' + to_render.slice(prev+2, i) + '</del>'+'</font>'+ " ";
		}
		else if(to_render[prev+1] =='-'){
			next_string = '<font color="green">'+ to_render.slice(prev+2, i) + '</font>' + " ";
		}
		else{
			next_string = to_render.slice(prev+1, i) + " ";
		}
		prev = i;
	}
	
	
	final += next_string;
	
	//document.getElementById("tracked").innerHTML += next_string ;
}
console.log(final)
