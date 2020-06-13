setTimeout(myFunction, 5000);
    function myFunction() {
        var buttons_arena = document.getElementsByClassName("css-1dbjc4n r-1gkumvb r-1efd50x r-5kkj8d r-18u37iz r-9qu9m4");
        console.log(buttons_arena);
        // alert("inside");
        var btn = document.createElement("button");
        var image = document.createElement("img");
        var imgURL = chrome.runtime.getURL('logo/16.PNG')
        // image.setAttribute('src', chrome.runtime.getURL('128.PNG'));
        image.src = imgURL;
		var link = document.createElement('a');
        var pageurl = window.location.href;
        var parts = pageurl.split('/');
		link.href = 'http://localhost:5000/results?username='+parts[3]+'&id='+parts[5];
		// image.appendChild(link);
        // btn.innerHTML = "Trumour";
        btn.appendChild(image);
        link.appendChild(btn);
        link.setAttribute('style', 'margin-left: auto; background:transparent; border-radius:50%;');
        link.setAttribute('class', 'trumour_btn');
        link.setAttribute('id', 'trumour_btn');
        link.setAttribute('target','_blank');
        // btn.style.backgroundImage = "url('logo/128.PNG')";
        // btn.innerHTML = '<img src="logo/16.png" />';
        // btn.innerHTML = '<img src="images\ok.png" />';
        var globalVariable={
            x: buttons_arena[0].baseURI
         };
   //      btn.onclick = function() {
   //          // chrome.tabs.create({url: 'http://www.google.com', active: false});
            
   //          var url = buttons_arena[0].baseURI;
   //          // chrome.runtime.openOptionsPage();
   //          // if (chrome.runtime.openOptionsPage) {
   //          //     // chrome.runtime.openOptionsPage();
   //          //     window.open(chrome.tabs.create('chrome://result.html'));
   //          //   } else {
   //          //     window.open(chrome.runtime.getURL('result.html'));
   //          //   }
   //          // resultpg = "http://localhost/Trumour/result_page.html";
   //          // window.open(resultpg);
   //          // chrome.storage.sync.set(function() {
			// // 	var resultpg = "chrome-extension://"+chrome.runtime.id+"/result.html";
			// //     chrome.tabs.create({url: resultpg});
   //          // });
   //          // chrome.tabs.create({ 'url': 'chrome://extensions/?options=' + chrome.runtime.id });
   //          // setTimeout(display(url), 2000);
   //              // chrome.browserAction.setPopup({
   //              //    popup:"http://localhost/Trumour/result_page.html"
   //              // });
   //              // chrome.tabs.create({url:"http://localhost/Trumour/result_page.html"});
   //              // chrome.browserAction.onClicked.addListener(function(activeTab){
   //                  // var newURL = "http://stackoverflow.com/";
   //                  // chrome.tabs.create({ url: newURL });
   //              //   });
            
   //          // var url = window.location.href;

            
   //          // var baseURL = "https://5000-b75f3c64-430e-49fc-87fd-3661a860b56f.ws-us02.gitpod.io/find/";
   //          // const urlParams = `tweet=${url}`;
   //          // // var probability = httpGet(tweet);
   //          // var xhttp = new XMLHttpRequest();

   //          // xhttp.onreadystatechange = function() {
   //          //     if (this.readyState == 4 && this.status == 200) {
   //          //         // a = JSON.parse(this.responseText);
   //          //         console.log(this.responseText);
   //          //     }
   //          //   };


   //          // xhttp.open("POST", baseURL, false); // false for synchronous request
   //          // xhttp.setRequestHeader("Content-type", "application/json");
   //          // xhttp.send(urlParams);

   //          // xhttp.onreadystatechange = function() { // Call a function when the state changes.
   //          //     if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
   //          //         console.log("Got response 200!");
   //          //     }
   //          // }
   //          // console.log("Tweet: Posted");

   //          // $.ajax({
   //          //     type: "POST",
   //          //     url: "https://5000-b75f3c64-430e-49fc-87fd-3661a860b56f.ws-us02.gitpod.io/find/",
   //          //     data: { url: newURL },
   //          //     success: function(data){
   //          //       // ...
   //          //     }
   //          //   });

   //          // var xhttp = new XMLHttpRequest();
   //          // xhttp.onreadystatechange = function() {
   //          //     if (this.readyState == 4 && this.status == 200) {
   //          //         document.getElementById("demo").innerHTML = this.responseText;
   //          //     }
   //          // };
   //          // xhttp.open("GET", "server_link"+url, true);
   //          // xhttp.send();
            
   //          console.log("URL : "+url);
   //          // console.log("Probability: "+probability);
   //      }
        buttons_arena[0].appendChild(link);
    }

    // function display(url){
    //     console.log("here");
    //     var textb = document.getElementById('textb');
    //     textb.innerHTML = url;
    //     console.log("Textb: "+textb);
    // }

    // function httpGet(tweet){
        // var xhttp = new XMLHttpRequest();
        // xhttp.onreadystatechange = function() {
        //     if (this.readyState == 4 && this.status == 200) {
        //         a = JSON.parse(this.responseText);
        //         console.log(a);
        //     }
        //   };
        // xhttp.open("POST", "https://5000-b75f3c64-430e-49fc-87fd-3661a860b56f.ws-us02.gitpod.io/find/", true); // false for synchronous request
        // xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        // xhttp.send("tweet="+tweet);
        // console.log("Tweet: Posted");
        // return xmlHttp.responseText;

        // xhttp.open("POST", " http://127.0.0.1:5000/find/", true);
        // xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        // xhttp.send("tweet="+tweet);
    // }

    // function loadDoc() {
    //     var xhttp = new XMLHttpRequest();
    //     xhttp.onreadystatechange = function() {
    //       if (this.readyState == 4 && this.status == 200) {
    //         document.getElementById("demo").innerHTML = this.responseText;
    //       }
    //     };
    //     xhttp.open("POST", "demo_post2.asp", true);
    //     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //     xhttp.send("fname=Henry&lname=Ford");
    //   }
// var s = document.createElement('script');
// // TODO: add "script.js" to web_accessible_resources in manifest.json
// s.src = chrome.runtime.getURL('script.js');
// s.imgURL = chrome.runtime.getURL('128.PNG');
// // s.onload = function() {
// //     this.remove();
// // };
// (document.head || document.documentElement).appendChild(s);
// (document.head || document.documentElement).appendChild(imgURL);
// chrome.runtime.onMessage.addListener(function(request, sender, sendResponse)    {
//     console.log(request.command);

//     var div = document.createElement('div');
//     var label = document.createElement('span');
//     label.textContent = "Hello, world";
//     div.appendChild(label);
//     document.body.appendChild(div);

//     sendResponse({result: "success"});
// });

/*
<div class="css-1dbjc4n r-1gkumvb r-1efd50x r-5kkj8d r-18u37iz r-9qu9m4">
    <div class="css-1dbjc4n">
        <a>
            <div class="css-1dbjc4n r-xoduu5 r-1udh08x">
                <span class="css-901oao css-16my406 r-1qd0xha r-vw2c0b r-ad9z0x r-bcqeeo r-d3hbe1 r-1wgg2b2 r-axxi2z r-qvutc0">
                    <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                        1.6K
                    </span>
                </span>
            </div>
            <span class="css-901oao css-16my406 r-1re7ezh r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                    Retweets
                </span>
            </span>
        </a>
    </div>
    <div class="css-1dbjc4n r-1joea0r">
        <a>
            <div class="css-1dbjc4n r-xoduu5 r-1udh08x">
                <span class="css-901oao css-16my406 r-1qd0xha r-vw2c0b r-ad9z0x r-bcqeeo r-d3hbe1 r-1wgg2b2 r-axxi2z r-qvutc0">
                    <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                        6.1K
                    </span>
                </span>
            </div>
            <span class="css-901oao css-16my406 r-1re7ezh r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">
                    Likes
                </span>
            </span>
        </a>
    </div>
</div>
*/
// css-1dbjc4n r-18u37iz r-d0pm55 r-thb0q2