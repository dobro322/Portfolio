<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-layout hidden-sm-and-up justify-center row wrap>
        <div><v-btn flat large color="purple" @click="filter = 'abtx'"><p>Очки</p></v-btn></div>
        <div><v-btn flat large color="green" @click="filter = 'surf'"><p>Найдено</p></v-btn></div>
        <div><v-btn flat large color="orange" @click="filter = 'messages'"><p>Сообщений</p></v-btn></div>
      </v-layout>
      <v-layout class="noselect" row wrap>
        <v-flex v-show="users">
          <v-layout class="noselect" row wrap>
            <v-flex lg8 md10 offset-md1 mb-1 offset-lg2 xs12 >
              <v-layout hidden-sm-and-down align-center text-xs-left texs-md-center row wrap>
                <v-flex md1 xs12 class="subheading">
                  <p>№</p>
                </v-flex>
                <v-flex md5 xs12 class="subheading">
                  <p>Участник</p>
                </v-flex>
                <v-flex @click="filter = 'abtx'" class="sorting subheading" md2 xs12>
                  <p><span><v-icon small color="orange" v-if="filter==='abtx'">filter_list</v-icon></span>Абиткоинов</p>
                </v-flex>
                <v-flex @click="filter = 'surf'" class="sorting subheading" md2 xs12>
                  <p><span><v-icon small color="orange" v-if="filter==='surf'">filter_list</v-icon></span>Найдено</p>
                </v-flex>
                <v-flex @click="filter = 'messages'" class="sorting subheading" md2 xs12>
                  <p><span><v-icon small color="orange" v-if="filter==='messages'">filter_list</v-icon></span>Сообщений</p>
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex lg8 md10 offset-md1 mb-1 offset-lg2 xs12 v-for="(user, index) in sorted_users" :key="index">
              <v-card>
                <v-layout align-center pa-2  text-xs-left texs-md-center row wrap>
                  <v-flex md1 class="display-1"><p>{{index + 1}}</p></v-flex>
                  <v-flex md5 xs12>
                    <v-layout text-xs-left texs-md-center align-center row wrap>
                      <div class="hidden-xs-only">

                        <v-avatar
                          size="50px"
                        >
                          <v-img :src="user.info.pic" alt="alt"></v-img>
                        </v-avatar>
                      </div>
                      <div class="headline" md8 xs12>
                        <router-link  style="text-decoration:none" :to="'/Companions/Team/' + user.info.vk"><p>{{ user.info.name }}</p></router-link>
                      </div>
                    </v-layout>
                  </v-flex>

                  <v-flex class="headline" md2 xs12>
                    <p>{{ user.score.abtx.amount }}</p>
                  </v-flex>

                  <v-flex class="headline" md2 xs12>
                    <p>{{ user.score.surf }}</p>
                  </v-flex>

                  <v-flex class="headline" md2 xs12>
                    <p>{{ user.score.messages }}</p>
                  </v-flex>

                </v-layout>
              </v-card>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

  export default {
    computed:{
      sorted_users(){
        if(this.filter === 'abtx')
          return this.users.sort((a,b) => {return a.score[this.filter].amount > b.score[this.filter].amount ? -1 : 1})
        return this.users.sort((a,b) => {return a.score[this.filter] > b.score[this.filter] ? -1 : 1})
      }
    },
    created(){
      const data = {
        filter: 'score,info'
      }
      axios.get('https://ocheredsut.ru/api/1/team/', {params: data}).then((resp) => {
        var temp_users = resp.data
        for (var user of temp_users) {
          user.show = false;
          user.info.name = user.info.name.split(' ').slice(0, 2).join(' ', 2)
          const reducer = (accumulator, currentValue) => accumulator + currentValue;
          user.score.surf = user.score.surf.length > 0 ? user.score.surf.map(a => {return a.amount}).reduce(reducer) : 0
          user.score.messages = user.score.messages.length > 0 ? user.score.messages.map(a => {return a.amount}).reduce(reducer) : 0
        }
        this.users = temp_users
      })
    },
    data(){
      return {
        filter: "abtx",
        users: []
      }
    },
    methods:{
    }
  }
</script>

<style>

.sorting:hover {
  cursor: pointer;
}
</style>
