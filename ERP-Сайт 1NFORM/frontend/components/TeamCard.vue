<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex text-xs-center fill-height class="display-1" v-if="!loaded">
        <v-layout align-center text-xs-center justify-center row wrap>
          <p>Загрузка...</p>
        </v-layout>
      </v-flex>
      <v-flex  v-else lg3 md4 sm6 xs12 v-for="(user, index) in users" :key="index">
        <v-card hover min-height="250px"  @click="get_user_score(user)" :class="faculty_class(user.info.faculty) +' rounded ma-4 py-4'">
          <v-layout class="noselect" align-center text-xs-center row wrap>
            <v-flex xs12>
              <v-avatar size="100">
                <v-img max-height="150" :src="user.info.pic"></v-img>
                <a  :href="'https://vk.com/id' + user.info.vk" target="_blank" style="text-decoration:none; position: absolute; top:70px; left:70px"><img style="height:30px"src="https://1.bp.blogspot.com/-2jQQ7FrGtGU/XFsqyrZRIwI/AAAAAAAAH3Y/UZ_DqDQeCdM9aTZKyE2gStTAn3Je3jNbACK4BGAYYCw/s1600/logo%2Bvk.png"></img></a>
              </v-avatar>
            </v-flex>
            <v-flex class="headline" xs12>
              <p>{{ user.info.name }}</p>
            </v-flex>
            <v-flex>
              <p>{{ user.info.phone }}</p>
            </v-flex>
            <v-flex xs12>
              <v-layout v-if="check_role() ==='794'" row justify-center wrap>
                <v-flex xs4 v-for="n in user.rate">
                  <p style="font-size:25px">🌚</p>
                </v-flex>
                <v-flex v-if="user.role" xs12>
                  <p style="font-size:15px">{{ user.role }}</p>
                </v-flex>
              </v-layout>
              <v-layout row wrap>
                <v-flex class="caption" v-for="dep in user.departments">
                  <p>{{ dep }}</p>
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex v-if="user.show && user.score" xs12>
              <v-layout row wrap>
                <v-flex pt-4 xs12 class="headline"><p>Собеседник</p></v-flex>
                <v-flex xs12 md6>
                  <v-layout row wrap>
                    <v-flex xs12>
                      <p>Сообщений</p>
                    </v-flex>
                    <v-flex class="display-1" xs12>
                      <p class="museo700">{{ summ_messages(user) }}</p>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex xs12 md6>
                  <v-layout row wrap>
                    <v-flex xs12>
                      <p>Слов</p>
                    </v-flex>
                    <v-flex class="display-1"  xs12>
                      <p class="museo700">{{ summ_words(user) }}</p>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex xs12 class="headline"><p>Сёрфер</p></v-flex>
                <v-flex xs12 md6>
                  <v-layout row wrap>
                    <v-flex xs12>
                      <p>С факультета</p>
                    </v-flex>
                    <v-flex class="display-1" xs12>
                      <p class="museo700">{{ surfed_faculty(user) }}</p>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex xs12 md6>
                  <v-layout row wrap>
                    <v-flex xs12>
                      <p>С универа</p>
                    </v-flex>
                    <v-flex class="display-1"  xs12>
                      <p class="museo700">{{ surfed_other(user) }}</p>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex class="headline">
                  <p>Счёт</p>
                </v-flex>
                <v-flex xs12>
                  <v-btn class="headline purple--text text--lighten-1 font-weight-bold" flat><v-icon left>monetization_on</v-icon><p class="museo700">{{ user.score.abtx.amount }}</p></v-btn>
                </v-flex>
                <v-flex xs12>
                  <v-btn color="orange" flat :to="'Team/'+ user.info.vk"><p>Подробнее</p></v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card>
        <v-flex v-if="check_role() === '794' && user.show" xs12>
          <v-layout text-xs-center wrap>
            <v-flex xs12>
              <v-autocomplete
                v-model="user.departments"
                :items="departments"
                prepend-icon="how_to_reg"
                label="Отделы"
                multiple
              ></v-autocomplete>
            </v-flex>
            <v-flex xs12>
              <v-btn dark @click="confirm_deps(user)"><p>Подтвердить</p></v-btn>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex v-if="check_role() === '794' && user.show" xs12>
          <v-layout text-xs-center wrap>
            <v-flex xs12>
              <v-autocomplete
                v-model="user.role"
                :items="roles"
                prepend-icon="how_to_reg"
                label="Уровень доступа"
              ></v-autocomplete>
            </v-flex>
            <v-flex xs12>
              <v-btn dark @click="confirm_role(user)"><p>Подтвердить</p></v-btn>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

  export default {
    methods:{
      confirm_deps(user){
        const data = {
          departments: user.departments,
          vk: user.info.vk
        }
        axios.put('https://ocheredsut.ru/api/1/admin/user_department', data).then((resp) =>{
          user.departments = resp.data.departments
        })
      },
      confirm_role(user){
        const data = {
          role: user.role,
          vk: user.info.vk
        }
        axios.put('https://ocheredsut.ru/api/1/admin/role', data).then((resp) =>{
          user.role = resp.data.role
        })
      },
      check_role(){
        return localStorage.role
      },
      delete_user(user){
        axios.delete('https://ocheredsut.ru/api/1/team/' + user.info.vk).then((resp) => {
          this.users.splice(this.users.indexOf(user), 1)
        })
      },
      surfed_faculty(user){
        return user.score.surf.find(a=>{return a.faculty === user.info.faculty}) ? user.score.surf.find(a=>{return a.faculty === user.info.faculty}).amount : 0
      },
      surfed_other(user){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return user.score.surf.map(a=>{return a.amount})[0] ? user.score.surf.map(a=>{return a.amount}).reduce(reducer) : 0
      },
      summ_messages(user){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return user.score.messages.map(a=>{return a.amount})[0] ? user.score.messages.map(a=>{return a.amount}).reduce(reducer) : 0
      },
      summ_words(user){
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        return user.score.messages.map(a=>{return a.words})[0] ? user.score.messages.map(a=>{return a.words}).reduce(reducer) : 0
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
      },
      get_user_score(user){
        const data = {
          filter: 'score'
        }
        axios.get('https://ocheredsut.ru/api/1/team/' + user.info.vk, {params: data}).then((resp) => {

          user.score = resp.data.score
          user.show = !user.show;
        })
      },
    },
    created(){
      const data = {
        filter: 'info,departments'
      }
      if(this.check_role() === '794') data.filter+=',role'
      axios.get('https://ocheredsut.ru/api/1/team/', {params: data}).then((resp) => {
        var temp_users = resp.data
        for (var user of temp_users) {
          user.show = false;
          user.info.name = user.info.name.split(' ').slice(0, 2).join(' ', 2)
        }
        this.users = temp_users
        this.loaded = true
      })
    },
    data(){
      return{
        departments: [
          "Собеседники",
          "Серфинг",
          "Фильтрация",
          "SMM",
          "Event",
          "Фандрайзинг",
          "Приемная комиссия"
        ],
        roles: [
          "204",
          "224",
          "724",
          "794",
        ],
        loaded: false,
        users:[]
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

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
}
</style>
