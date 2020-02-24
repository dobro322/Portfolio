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

      <div>
      <v-toolbar dark class="bgradient noselect">
        <v-toolbar-side-icon class="hidden-lg-and-up" @click="drawer = !drawer"></v-toolbar-side-icon>

        <router-link  to="/Quests" ><img class="hidden-sm-and-down" style="height:25px" src="./assets/img/logo.png" alt="avatar"></img></router-link>
        <v-toolbar-items class="pl-2 hidden-md-and-down">
          <v-btn style="border-right:solid; border-width:2px; border-color:#ecf0f1" :key="dep.name" v-for="dep in menu" router block :to="dep.path" flat >
            <div class="px-2"><p class="museo700">{{ dep.name }}</p></div>
          </v-btn>
        </v-toolbar-items>
        <v-spacer></v-spacer>

        <p style="font-size:25px" class="text-truncate museo700 hidden-sm-and-down pr-4 grey--text text--darken-3">{{ user.info.name.split(' ')[0] }} {{ user.info.name.split(' ')[1] }}</p>
        <router-link :to="'/Companions/Team/' + user.info.vk">
          <v-avatar>
              <v-img :src="user.info.pic" alt="avatar"></v-img>
          </v-avatar>
        </router-link>
      </v-toolbar>
      <router-view ></router-view>
      </div>
      <!-- <Logging :visible="!logged" @code="send_code"></Logging> -->
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import Logging from './views/Logging.vue'
import format from 'date-fns/format'

export default {
  name: 'App',
  components: {
    Logging
  },
  methods:{
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
      axios.put("http://127.0.0.1:5000/endorfin/1/account/", data).then((resp)=>{
        this.user.settings = resp.data.settings
      })
    },
    authorize(){
      const data = {
        filter: 'info,news,settings,token,role,score.abtx,departments',
      }
      axios.defaults.headers.common['Authorization'] = localStorage.token
      axios.get('http://127.0.0.1:5000/endorfin/1/account/', {params: data}).then((resp)=>{

      })
    },
    send_code(data){
      axios.post('http://127.0.0.1:5000/endorfin/1/login/', data).then((resp)=>{
        localStorage.token = resp.data.token
        this.authorize()
        this.$router.replace('/main')

      })
    }
  },
  computed:{
  },
  data(){
    return{
      notification_dialog: false,
      loaded: false,
      logged: false,
      temp_pic: "",
      menu:[
        {
          name: "Бронь",
          path: "/reservation"
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
	font-family: "GothamMedium";
	src: url('./assets/fonts/GothamPro-Medium.ttf');
}

.bgradient {
  background:linear-gradient(-2deg, #7F00D1, #2D0059)
}

p {
  font-family: 'GothamMedium';
  line-height: 1.5;
  margin-bottom: 0;
  vertical-align: middle;
}

.scroll {
      overflow-y: scroll;
    }

.rounded {
  border-radius: 10px;
  overflow: hidden;
}

.noselect {
  text-decoration: none;
  cursor: default;
}

v-navigation-drawer {
    height: 100%
}

/* width */
::-webkit-scrollbar {
  width: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

</style>
