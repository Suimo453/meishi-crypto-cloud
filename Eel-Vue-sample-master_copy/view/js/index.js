var app = new Vue({
  el: "#root",
  template: `
    <div class="main">
      <form class="registrationform" v-on:submit.prevent="onSubmit">
        <h1>登録</h1>
        <div class="wrapper">
            <label for="companylabel">会社名</label>
            <input type="text" name="companyname" id="company" placeholder="例）株式会社〇〇〇" v-model="company" required>
        </div>
        <div class="wrapper">
            <label for="namelabel">氏名</label>
            <input type="text" name="name" id="name" placeholder="例）鈴木　太郎" v-model="name">
        </div>
        <div class="wrapper">
            <label for="imagelabel">写真</label>
            <input type="file" name="image" id="image" accept="image/jpeg, image/png, image/gif" multiple v-model="image" v-on:change="changeImg">
        </div>
        <div class="wrapper">
            <input type="submit" value="送信する">
        </div>
      </form>
      <div>{{company}}</div>
      <div>{{name}}</div>

      <form action="#" method="post" v-on:submit.prevent="onSearch">
          <h1>検索</h1>
          <input type="search" name="search" id="search" placeholder="会社名" v-model="query_company">
          <input type="search" name="search" id="search" placeholder="氏名" v-model="query_name">
          <input type="submit" name="submit" id="submit" value="検索">
          <h2>検索結果</h2>
          <div id="result" v-for="meisi in meisi_list">
            <p>会社名：
              <div id="result_company">{{ meisi.company }}</div>
            </p>
            <p>氏名：
              <div id="result_name">{{ meisi.name }}</div>
            </p>
            <p>画像：
              <img v-bind:src="meisi.image" alt="" />
            </p>
          </div>
      </form>
    </div>
    `,
  data() {
    return {
      company: "",
      name: "",
      image: "",
      query_company: "",
      query_name: "",
      meisi_list: []
    };
  },
  mounted() {},
  methods: {
    changeImg(e) {
      let that = this
      //that.loadedImage = e.target.files[0]
      let reader = new FileReader()
      reader.onload = function (e) {
          that.image = e.target.result;
      }
      reader.readAsDataURL(e.target.files[0]);
    },
    async onSubmit() {
      //登録フォームのsubmitが押された時の挙動
      var enccompany = await eel.enctag(this.company)()
      var encname = await eel.enctag(this.name)()
      var image = await eel.enc(this.image)()
      var company = await eel.enc(this.company)()
      var name = await eel.enc(this.name)()

      const postData = {
        company,
        name,
        image,
        enccompany,
        encname
      };

      console.log("postDate ",postData)

      fetch("http://127.0.0.1:5004/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
        .then((res) => res)
        .then((data) => {
          console.log(data);
          // ここで必要に応じて何らかの処理を行う
        })
        .catch((error) => {
          console.error("エラー:", error);
        });
    },

    async onSearch() {
      //検索クエリを取得した際の挙動
      var query_company = "";
      var query_name = "";

      if (this.query_company){
        query_company = await eel.trap(this.query_company)()
      }
      if (this.query_name){
        query_name = await eel.trap(this.query_name)()
      }

      const self = this
      
      const postData = {
        company: query_company,
        name: query_name
      }

      fetch("http://127.0.0.1:5004/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
        .then((res) => res.json())
        .then(async (data) => {
          var result = []
          console.log(data);
          for (var meisi of data){
            var name = await eel.dec(meisi.name)()
            var company = await eel.dec(meisi.company)()
            var image = await eel.dec(meisi.image)()
            result.push({
              name,company,image
            })
          }
          self.meisi_list = result
          // ここで必要に応じて何らかの処理を行う
        })
        .catch((error) => {
          console.error("エラー:", error);
        });
    },
  },
});
