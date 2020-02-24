<template>
  <v-container fluid>
    <v-layout v-if="user"  justify-center row wrap>
      <v-flex d-flex lg9 md8 sm12 px-1 order-xs2 order-md1>
        <v-card hover class="rounded">
          <v-card-title class="display-1"><p>Статистика</p></v-card-title>
          <v-layout pa-4 row wrap>
            <v-flex xs12>
              <p style="font-size:30px">Серфинг</p>
              <apexchart class="hidden-sm-and-down" width="100%" height="200px" type="line" :options="surf_categories" :series="surf_series"></apexchart>
            </v-flex>

            <v-flex md4 xs12 class=""><p>Найдено с факультета <span class="museo900" style="font-size:35px"><br>{{surfed_faculty}}</span></p></v-flex>
            <v-flex md4 xs12 class=""><p>Найдено с других <span class="museo900" style="font-size:35px"><br>{{surfed_other - surfed_faculty}}</span></p></v-flex>
            <v-flex md4 xs12 class=""><p>Найдено всего <span class="museo900" style="font-size:35px"><br>{{surfed_other}}</span></p></v-flex>

            <v-flex xs12>
              <p style="font-size:30px">Собеседник</p>
              <apexchart class="hidden-sm-and-down" width="100%" height="200px" type="line" :options="chat_categories" :series="chat_series"></apexchart>
            </v-flex>

            <v-flex md4 xs12 class=""><p>Написано сообщений <span class="museo900" style="font-size:35px"><br>{{summ_messages}}</span></p></v-flex>
            <v-flex md4 xs12 class=""><p>Написано слов <span class="museo900" style="font-size:35px"><br>{{summ_words}}</span></p></v-flex>
            <v-flex md4 xs12 class=""><p>Слов на сообщение <span class="museo900" style="font-size:35px"><br>{{summ_messages === 0 ? 0 : parseInt(summ_words / summ_messages)}}</span></p></v-flex>

          </v-layout>
        </v-card>
      </v-flex>
      <v-flex d-flex lg3 md4 sm12 px-1 order-xs1 order-md2>
        <v-layout d-flex row wrap>
          <v-flex v-if="user.info" d-flex pb-2>
            <v-card hover class="rounded">
              <v-layout :class="faculty_class(user.info.faculty)" text-xs-center align-center pa-4 row wrap>

                <v-flex xs12 md6 order-xs1 order-md2>
                  <v-avatar size="120">
                    <v-img :src="user.info.pic"></v-img>
                    <a :href="'https://vk.com/id' + user.info.vk" target="_blank" style="text-decoration:none; position: absolute; top:85px; left:85px"><img style="height:35px"src="https://1.bp.blogspot.com/-2jQQ7FrGtGU/XFsqyrZRIwI/AAAAAAAAH3Y/UZ_DqDQeCdM9aTZKyE2gStTAn3Je3jNbACK4BGAYYCw/s1600/logo%2Bvk.png"></img></a>
                  </v-avatar>
                </v-flex>

                <v-flex xs12 md6 order-xs2 order-md1>
                  <v-layout style="text-align:right" text-xs-center text-md-right row wrap>
                    <v-flex xs12 style="font-size:30px"><p>{{user.info.name}}</p></v-flex>

                    <v-flex xs12><a :href="'tel:' + user.phone"><p>{{user.info.phone}}</p></a></v-flex>
                  </v-layout>
                </v-flex>

                <v-flex pt-4 xs12 md12 order-xs3 order-md3>
                  <v-layout row wrap>
                    <v-flex class="subheading" v-for="dep in user.departments">
                      <p>{{dep}}</p>
                    </v-flex>
                  </v-layout>
                </v-flex>

              </v-layout>
            </v-card>
          </v-flex>
          <v-flex d-flex :class="$vuetify.breakpoint.xs ? 'pb-2' : ''">
            <v-card hover class="rounded">
              <v-layout pa-4 row wrap>
                <p style="font-size:30px">Новостная лента</p>
                <v-flex xs12 v-for="achieve in user.news.filter(a=>{return a.type != 'personal'})">
                  <p><span>{{formattedDate(achieve.date * 1000)}}</span> выполнил задание <br class="hidden-sm-and-up"><span style="font-size:20px">"{{achieve.title}}"</span></p>
                  <v-divider></v-divider>
                </v-flex>
              </v-layout>
            </v-card>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
    <!-- <button type="button" @click="notify">Show notification</button> -->
  </v-container>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import axios from 'axios'
import format from 'date-fns/format'

  export default {
    computed: {
      surfed_faculty(){
        return this.user.score.surf.find(a=>{return a.faculty === this.user.info.faculty}) ? this.user.score.surf.find(a=>{return a.faculty === this.user.info.faculty}).amount : 0
      },
      surfed_other(){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return this.user.score.surf.map(a=>{return a.amount}).length > 0 ? this.user.score.surf.map(a=>{return a.amount}).reduce(reducer) : 0
      },
      summ_messages(){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return this.user.score.messages.map(a=>{return a.amount}).length > 0 ? this.user.score.messages.map(a=>{return a.amount}).reduce(reducer) : 0
      },
      summ_words(){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return this.user.score.messages.map(a=>{return a.words}).length > 0 ? this.user.score.messages.map(a=>{return a.words}).reduce(reducer) : 0
      },
      surf_categories(){
        return {
          chart: {
            id: 'vuechart-example',
            toolbar:{
              show:false
            }
          },
          xaxis: {
            categories: this.user.surfing ? this.user.surfing.map(a=>{return this.formattedDate(Object.keys(a)[0])}) : []
          }
        }
      },
      surf_series(){
        return [{
          name: 'Найдено',
          data: this.user.surfing ? this.user.surfing.map(a=>{return a[Object.keys(a)[0]].date_found}) : []
        }]
      },
      chat_categories(){
        return {
          chart: {
            id: 'vuechart-example',
            toolbar:{
              show:false
            }
          },
          xaxis: {
            categories: this.user.chatting ? this.user.chatting.map(a=>{return this.formattedDate(Object.keys(a)[0])}) : []
          }
        }
      },
      chat_series(){
        return [{
          name: 'Сообщений',
          data: this.user.chatting ? this.user.chatting.map(a=>{return a[Object.keys(a)[0]].count }) : []
        }]
      }
    },
    components: {'apexchart': VueApexCharts,},
    created(){
      const data = {
        extended: true,
        filter: 'info,departments,score,news',
      }
      axios.get('https://ocheredsut.ru/api/1/team/'+this.$route.params.id, {params: data}).then((resp) => {
        this.user = resp.data
      })
    },
    data(){
      return {
        user: null
      }
    },
    methods:{
      formattedDate(arg){
        return arg? format(arg, 'D.MM') : ''
      },
      notify () {
      // https://developer.mozilla.org/en-US/docs/Web/API/Notification/Notification#Parameters
        this.$notification.show('Hello World', {
          body: 'This is an example!'
        }, {})
      },
      faculty_class(arg){
        const facs = [
          {
            name:"ИСиТ",
            class:"isit"
          },
          {
            name:"РТС",
            class:"rts"
          },
          {
            name:"ИКСС",
            class:"ikss"
          },
          {
            name:"ЦЭУБИ",
            class:"fey"
          },
          {
            name:"ВУЦ",
            class:"ivo"
          },
          {
            name:"ГФ",
            class:"gf"
          },
          {
            name:"ИНО",
            class:"ino"
          },
          {
            name:"СПбКТ",
            class:"spbkt"
          },
          {
            name:"ФП",
            class:"fp"
          }
        ]
        return facs.find(a=>{return a.name === arg}).class
      }
    }
  }
</script>

<style>
.isit{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/ISiT.png')
}

.rts{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/RTS.png')
}

.ikss{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/IKSS.png')
}

.gf{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/GF.png')
}

.ivo{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/IVO.png')
}

.fey{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/FEY.png')
}

.spbkt{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/SPbKT.png')
}

.fp{
  background-origin:padding-box;
  background-size:150px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('../assets/img/FP.png')
}

.ino{
  background-origin:padding-box;
  background-size:100px;
  background-clip: padding-box;
  background-position: top right;
  background-image: linear-gradient(rgba(255,255,255,.6),
                    rgba(255,255,255,.6)),
                    url('')
}
</style>
