<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12>
        <v-text-field
          label="Код"
          autofocus
          ref="code"
          v-model="inp"
          @keyup.enter.native="find_person"
        ></v-text-field>
      </v-flex>
      <v-flex xs6 offset-xs3 v-if="user.name">
        <v-card>
          <v-card-title>
            <div class="display-2"><p>Билет №{{user.id}}</p></div>
          </v-card-title>
          <v-card-text>
            <v-layout text-xs-center justify-space-around align-center row wrap>
              <v-flex xs12>
                <v-avatar
                  size="300px"
                >
                  <v-img :src="user.kib_pic"></v-img>
                </v-avatar>
                <v-avatar
                  size="300px"
                >
                  <v-img :src="user.pic"></v-img>
                </v-avatar>
              </v-flex>
              <v-flex class="display-2">
                <p>{{user.name.split(" ")[0]}}</p>
                <p>{{user.name.split(" ")[1]}}</p>
                <p>{{user.name.split(" ")[2]}}</p>
              </v-flex>
            </v-layout>
            <v-layout class="pt-4" text-xs-center row wrap>
              <v-flex class="headline">
                <p>Факультет: {{user.faculty}}</p>
              </v-flex>
              <v-flex class="headline">
                <p>Дата рождения: {{user.bdate}}</p>
              </v-flex>
            </v-layout>
            <v-layout class="pt-4" text-xs-center row wrap>
              <v-flex class="green--text headline" v-if="user.arrived.state === false" xs12>
                <p>Предъявлен первый раз</p>
              </v-flex>
              <v-flex v-else class="red--text headline" xs12>
                <p>Уже был предъявлен {{formattedDate(user.arrived.date * 1000)}}</p>
                <br>
                <p>Проверил {{user.arrived.checked_by}}</p>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex v-else class="display-4 text-xs-center">
        <p>Не найден</p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import format from 'date-fns/format'

  export default {
    methods:{
      formattedDate(arg){
        return arg? format(arg, 'HH:mm:ss') : ''
      },
      find_person(){
        var t = ""
        if (this.inp.includes("-")) t = this.inp.slice(7)
        else t = this.inp
        axios.get("https://ocheredsut.ru/api/1/event/participant/" + t).then((resp) =>{
          this.user = resp.data
          this.inp = ""
          this.$refs.code.$el.focus()
        }).catch((resp)=>{
          this.user={}
          this.inp = ""
        })
      }
    },
    created(){
    },
    data(){
      return {
        user: {},
        inp: ""
      }
    }
  }
</script>

<style>

</style>
