<template>
  <v-app>
    <v-content>
      <v-navigation-drawer   dark v-model="drawer" absolute temporary>
        <v-list  :style="{height:'100vh', background: 'linear-gradient(rgba(0,0,0,.7),rgba(0,0,0,.7)), url(' + user.settings.menu_pic + ') 50% 100% /cover no-repeat' }">
          <v-list-tile avatar tag="div">
            <v-list-tile-avatar>
              <v-img :src="user.info.pic"></v-img>
            </v-list-tile-avatar>

            <v-list-tile-content>
              <v-list-tile-title><p class="museo700">{{ user.info.name }}</p></v-list-tile-title>
            </v-list-tile-content>

            <v-list-tile-action>
              <v-btn icon @click.stop="drawer = !drawer">
                <v-icon>chevron_left</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
          <v-divider></v-divider>

           <v-list-tile
             v-for="item in menu"
             :key="item.name"
           >
             <v-list-tile-content>
              <v-btn router class="ml-0 pl-2 text-capitalize headline rounded" large flat :to="item.path"><p style="width:220px" class="museo700">{{ item.name }}</p></v-btn>
             </v-list-tile-content>

           </v-list-tile>
           <v-dialog
             max-width="500px"
           >
             <div slot="activator" style="position: absolute; top: 90vh"> <v-btn flat>+ загрузить фон</v-btn> </div>
               <v-card dark>
                 <v-text-field
                   label="Введите URL"
                   v-model="temp_pic"
                   color="orange"
                   class="px-1 pt-4"
                 ></v-text-field>
                 <v-btn block color="green" dark @click="update_bg"><p>Подтвердить</p></v-btn>
               </v-card>
           </v-dialog>
         </v-list>
      </v-navigation-drawer>
      <div v-if="logged">
      <v-toolbar  class="noselect">
        <v-toolbar-side-icon class="hidden-lg-and-up" @click="drawer = !drawer"></v-toolbar-side-icon>
        <!-- <v-toolbar-tile>
          <p class="museo700" style="font-size:30px">1NFORM</p>
        </v-toolbar-tile> -->
        <router-link  to="/Quests" ><img class="hidden-sm-and-down" style="height:25px" src="./assets/img/logo.png" alt="avatar"></img></router-link>
        <v-toolbar-items class="pl-2 hidden-md-and-down">
          <v-btn style="border-right:solid; border-width:2px; border-color:#ecf0f1" :key="dep.name" v-for="dep in menu" router block :to="dep.path" flat >
            <div class="px-2"><p class="museo700">{{ dep.name }}</p></div>
          </v-btn>
        </v-toolbar-items>
        <v-spacer></v-spacer>

        <v-dialog
          max-width="500px"
          class="hidden-sm-and-up"
          v-model="notification_dialog"
        >
        <v-badge v-if="user.news" slot="activator" overlap color="warning" right>
          <div slot="badge" v-if="user.news.filter(a=>{return a.readed!=true}).length > 0">
            <p>{{user.news.filter(a=>{return a.readed!=true}).length}}</p>
          </div>
          <v-icon
            v-ripple="{center:true}"
            large
            color="grey lighten-1"
          >
            notifications
          </v-icon>
        </v-badge>
        <v-card>
          <div @click="notification_dialog = false" class="dialogclose"><v-icon large>close</v-icon></div>
          <v-layout row wrap>
            <v-flex xs12 class="text-xs-center py-3 noselect headline"><p>Уведомления</p></v-flex>
            <v-flex xs12 v-for="notification in sorted_news">
            <v-divider></v-divider>
              <v-layout :style="'background-color:' + (notification.readed ? 'white' : 'rgb(235,235,235)')" :class="notification.readed? 'usual pa-3' : 'clickable pa-3'" @click="read_notification(notification)" row wrap>
                <v-flex xs12 class="noselect headline">
                  <div><p>{{notification.title}}</p></div>
                </v-flex>
                <v-flex class="noselect"><p>{{notification.text}}</p></v-flex>
                <v-flex class="noselect grey--text"><p>{{formattedDate(notification.date)}}</p></v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card>
        </v-dialog>

        <v-menu v-if="user.news" class="hidden-xs-only" transition="scale-transition" :close-on-content-click="false" offset-y>
          <v-badge slot="activator" overlap color="warning" right>
            <div slot="badge" v-if="user.news.filter(a=>{return a.readed!=true}).length > 0">
              <p>{{user.news.filter(a=>{return a.readed!=true}).length}}</p>
            </div>
            <v-icon
              v-ripple="{center:true}"
              large
              color="grey lighten-1"
            >
              notifications
            </v-icon>
          </v-badge>

          <div>
            <v-card max-width="400px" min-width="300px" max-height="600px" style="overflow-y: auto;">
              <v-layout row wrap>
                <v-flex xs12 class="text-xs-center py-3 noselect headline"><p>Уведомления</p></v-flex>
                <v-flex xs12 v-for="notification in sorted_news">
                <v-divider></v-divider>
                  <v-layout :style="'background-color:' + (notification.readed ? 'white' : 'rgba(250, 211, 144, 0.3)')" :class="notification.readed? 'usual pa-3' : 'clickable pa-3'" @mouseover="read_notification(notification)" row wrap>
                    <v-flex xs12 class="noselect headline">
                      <div ><p>{{notification.title}}</p></div>
                    </v-flex>
                    <v-flex class="noselect"><p>{{notification.text}}</p></v-flex>
                    <v-flex class="noselect grey--text"><p>{{formattedDate(notification.date)}}</p></v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card>
          </div>
        </v-menu>

        <v-btn class="display-1 purple--text text--lighten-1 font-weight-bold" flat><v-icon left>monetization_on</v-icon><p style="line-height:1px" class="museo700">{{ user.score.abtx.amount }}</p></v-btn>
        <p style="font-size:25px" class="text-truncate museo700 hidden-sm-and-down pr-4 grey--text text--darken-3">{{ user.info.name.split(' ')[0] }} {{ user.info.name.split(' ')[1] }}</p>
        <router-link :to="'/Companions/Team/' + user.info.vk">
          <v-avatar>
              <v-img :src="user.info.pic" alt="avatar"></v-img>
          </v-avatar>
        </router-link>
      </v-toolbar>
      <Popup text="Hello world!" :open="false"></Popup>
      <router-view ></router-view>
      </div>
      <Logging :visible="!logged" @code="send_code"></Logging>
    </v-content>
  </v-app>
</template>

<script>
import Popup from './components/Popup.vue'
import axios from 'axios'
import Logging from './views/Logging.vue'
import format from 'date-fns/format'

export default {
  name: 'App',
  components: {
    Popup,
    Logging
  },
  methods:{
    read_notification(notific){
      axios.put("https://ocheredsut.ru/api/1/notifications/"+notific.id).then((resp)=>{
        notific.readed = true
      })
    },
    formattedDate(arg){
      return arg ? format(new Date(arg*1000), 'H:mm D.MM') : ''
    },
    check_role(){
      return localStorage.role
    },
    update_bg(){
      const data = {
        menu_pic: this.temp_pic,
        type: "settings"
      }
      axios.put("https://ocheredsut.ru/api/1/account/", data).then((resp)=>{
        this.user.settings = resp.data.settings
      })
    },
    authorize(){
      const data = {
        filter: 'info,news,settings,token,role,score.abtx,departments',
      }
      axios.defaults.headers.common['Authorization'] = localStorage.token
      axios.get('https://ocheredsut.ru/api/1/account/', {params: data}).then((resp)=>{
        this.user = resp.data
        localStorage.role = resp.data.role
        localStorage.name = resp.data.info.name
        localStorage.faculty = resp.data.info.faculty
        this.logged = true
        this.user.settings = this.user.settings
        this.user.news.sort((a,b)=>{return a.date > b.date ? -1: 1})
        if((resp.data.departments.includes("Фильтрация") || resp.data.departments.includes("Фандрайзинг")) && !this.menu.find(a=>{return a.name === "Отдел"}) ){
          this.menu.push({
            name: "Отдел",
            path: "/Additional"
          })
        }
        if(resp.data.role==='794'){
          this.menu.push({
            name: "Модерка",
            path: "/Moderate"
          })
        }
        if(resp.data.role>='724'){
          this.menu.push({
            name: "Билеты",
            path: "/Tickets"
          })
        }
        const data_news = {
          filter: 'news,score.abtx,departments,role'
        }
        setInterval(a=>{
          axios.get('https://ocheredsut.ru/api/1/account/', {params: data}).then((update_resp) => {
            for (var x in update_resp.data) {
              this.user[x] = update_resp.data[x]
            }
          })
        }, 5000)
      })
    },
    send_code(data){
      axios.post('https://ocheredsut.ru/api/1/login/', data).then((resp)=>{
        localStorage.token = resp.data.token
        this.authorize()
        this.$router.replace('/Quests')

      })
    }
  },
  computed:{
    sorted_news(){
      return this.user.news.sort((a,b) =>{return a.date > b.date ? -1 : 1})
    }
  },
  data(){
    return{
      notification_dialog: false,
      loaded: false,
      logged: false,
      temp_pic: "",
      menu:[
        {
          name: "Квесты",
          path: "/Quests"
        },
        {
          name: "Серфинг",
          path: "/Surfers"
        },
        {
          name: "Команда",
          path: "/Companions/Team"
        },
        {
          name: "Канбан",
          path: "/Kanbanviewer"
        },
      ],
      drawer: false,
      user: {
        info: {
          name: '',
          pic: ''
        },
        score: {
          abtx: {
            amount:0
          }
        },
        settings:{
          menu_pic:"https://pp.userapi.com/c850720/v850720450/fb289/mVxS7M0WW4w.jpg"
        }
      }
    }
  },
  created(){

      if(localStorage.token){

        this.authorize()
      }
  }
}
</script>

<style>
@font-face {
	font-family: "Museo";
	src: url('./assets/fonts/MuseoSansCyrl-500.otf');
}

@font-face {
	font-family: "Museo300";
	src: url('./assets/fonts/MuseoSansCyrl-300.otf');
}

@font-face {
	font-family: "Museo900";
	src: url('./assets/fonts/MuseoSansCyrl-900.otf');
}

@font-face {
	font-family: "Museo100";
	src: url('./assets/fonts/MuseoSansCyrl-100.otf');
}

@font-face {
	font-family: "Museo700";
	src: url('./assets/fonts/MuseoSansCyrl-700.otf');
}

.museo900 {
  font-family: 'Museo900'
}

.museo700 {
  font-family: 'Museo700'
}

.museo300 {
  font-family: 'Museo300'
}

.museo100 {
  font-family: 'Museo100'
}


p {
  font-family: 'Museo';
  line-height: 1.5;
  margin-bottom: 0;
  vertical-align: middle;
}

.clickable:hover{
  cursor:pointer;
}

.usual:hover{
  cursor: default;
}

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
}

.notific_tail {
  width: 30px;
  height: 30px;
  -moz-transform: rotate(40deg);
  -webkit-transform: rotate(40deg);
  -o-transform: rotate(40deg);
  -ms-transform: rotate(40deg);
  transform: rotate(40deg);
  border-style:solid;
  position: relative;
  top: -5px; left: 40px;
}

.dialogclose{
  position: absolute;
  right: 5px;
  top: 5px;
}

.rounded {
  border-radius: 10px;
  overflow: hidden;
}
v-navigation-drawer {
    height: 100%
}
</style>
