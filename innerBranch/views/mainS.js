
buildCategories = function(data, func){
    categories.innerHTML='';
    for(i=0;i<data.length;i++){
        but = document.createElement('button');
        but.className = 'list-group-item';
        but.type = 'button';
        but.innerHTML = data[i][1];
        but.id = data[i][0];
        but.onclick = function(){func(this.id);};
        if(but.id == '-1'){
            but.className = 'list-group-item list-group-item-info';
            but.onclick = function(){getMainCategories()}
        }
        categories.appendChild(but);
    }
};


buildPictures = function(data, func){
    console.log("Building pictures");
    pictures.innerHTML='';
    size = data.length;
    console.log(size);
    for(i=0;i<4;i++){
        curDiv = document.createElement('div');
        curDiv.className = '.col-sm-3';
        pictures.appendChild(curDiv);
        rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        curDiv.appendChild(rowDiv);
        for(j=0;j<8;j++){
            if(i*8 + j >= size ){
                return;
            }
            a = document.createElement('a');
            im = document.createElement('img');
            im.src = data[i*8+j][2];
            im.id = data[i*8+j][0];
            im.style = 'margin:7px;';
            im.onclick = function(){
                func(this.id);
            };
            a.appendChild(im);
            rowDiv.appendChild(a);
        }
    }

};





getSecondCat = function(currentCat){
  ws.send('getSubCategories,'+currentCat);
  ws.onmessage = function(e){
      console.log('getting entries');
      subCategory = JSON.parse(e.data);
      buildCategories(subCategory, getPictures);
  };
};

getPictures = function(catId){
    ws.send('getCatElems,'+catId);
    ws.onmessage = function(e){
        main = JSON.parse(e.data);
        buildPictures(main,selectPicture);
    };
};

getMainCategories = function(){
    ws.send('getMainCat,-1');
    ws.onmessage = function(e){
        main = JSON.parse(e.data);
        buildCategories(main,getSecondCat);
    };
};

selectPicture = function(pictId){
    ws.send('selPic,'+pictId);
    ws.onmessage = function(e){

    };
};
showFindings = function(data){
    if(data[0] == -1){
        console.log('no findings');
        head = document.createElement('h1');
        head.innerHTML = 'Sorry, we didnt find any route..';
        head.style = 'font-size:50px;color:white;padding:100px;';
        body.appendChild(head);
        return;
    }
    head = document.createElement('h1');
    body.innerHTML='';
    todolist = document.createElement('div');
    todolist.style = 'width:100%;text-algin:center;';
    head.innerHTML = 'Success!!!';
    head.style = 'font-size:50px;color:white;padding:100px;text-align:center;';
    todolist.appendChild(head);
    mylist = document.createElement('li');
    mylist.className = 'list-group';
    mylist.style = 'width:500px !important;margin-left:700px!important;';
    body.appendChild(todolist);
    todolist.appendChild(mylist);
    for(i = 0;i<data.length;i++){
        step = document.createElement('ul');
        step.innerHTML = 'take '+data[i][1]+' from '+data[i][2]+' and give him '+data[i][0];
        step.className = 'list-group-item';
        mylist.appendChild(step);
    }


};

submitDetails = function(){
    usernameinput = document.getElementById('unameform');
    email = document.getElementById('email');
    console.log(email.value);
    console.log(usernameinput.value);
    if(usernameinput.value == ""){
        alert("You should enter your name");
        return;
    }
    else if(email.value == ""){
        alert("You should enter your e-mail");
        return;
    }
    else if(!email.value.includes('@')){
        alert("Invalid mail address");
        return;
    }
    ws.send('submit,'+email.value+'*'+usernameinput.value);
    categories.innerHTML = '';
    pictures.innerHTML = '';
    progress = createProgressbar();
    forms = document.getElementsByClassName('form-inline')[0];
    forms.innerHTML="";
    ws.onmessage = function(e){
        prog = body.removeChild(document.getElementsByClassName('adjust')[0]);
        main = JSON.parse(e.data);
        showFindings(main);
    };
};

createProgressbar = function () {
    body = document.getElementsByClassName('body-container')[0];
    firs = document.createElement('div');
    firs.className = 'adjust';
    scnd = document.createElement('div');
    scnd.className = 'loader2';
    firs.appendChild(scnd);
    body.appendChild(firs);
};


















ws = new WebSocket("ws://107.191.62.204/websocket");
categoryData = null;
ws.onmessage = function(e) {
    console.log('Connected succesfully');
    categoryData = JSON.parse(e.data);
    buildCategories(categoryData, getSecondCat);
};
categories = document.getElementById('categories');
pictures = document.getElementById('pictures');
body = document.getElementsByClassName('body-container')[0];
