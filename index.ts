import axios from 'axios'

axios({
  url: 'http://192.168.1.1/cgi-bin/luci',
  proxy: false
})
  .then((res) => {
    console.log(res.data)
  })
  .catch((err) => {
    if (err.response.status === 403) {
      console.log(err.response.data)
    }
  })
