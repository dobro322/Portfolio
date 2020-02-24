<template>
  <v-container fluid>
    <v-layout text-xs-center wrap row>
      <v-flex d-flex xs12 sm6 md4 lg3 v-for="quest in quests_sorted" :key="quest.id">
        <v-card max-width="400px" style="display: flex; flex-direction: column;" class="rounded ma-1">
          <v-card height="10px" flat class="pa-1" :color="quest.completed ? 'green' : (get_date().getTime() > quest.date.getTime() ? 'red': 'orange')"></v-card>
          <div
          :style="'background-size: '+quest.pic.width+'px;background-position: '+(-quest.pic.left)+'px '+ (-quest.pic.top)+'px; background-image:url(' + quest.pic.url + ')'"
          class="hidden-xs-only"
          >
            <div style="height:250px;background-color:rgb(0,0,0,0.5)" >
              <v-layout v-if="quest.counting.count > 1" fill-height align-center row wrap>
                <v-flex class="white--text display-3 font-weight-bold">
                  <p>{{ quest.counting.current }}/{{ quest.counting.count }}</p>
                </v-flex>
              </v-layout>
            </div>
          </div>
          <v-card-title class="grow display-1 justify-center">
            <p class="museo700">{{quest.title}}</p>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="">
            <v-layout column wrap>
              <v-flex xs12 class="title font-weight-regular">
                <p>{{ quest.text }}</p>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions>
            <v-layout align-center row wrap>
              <v-flex md6 xs12 class="title font-weight-regular">
                <v-layout justify-center text-xs-center row wrap>
                  <p style="font-size:12px">{{quest.daily ? 'Ежедневное' : ''}}</p>
                </v-layout>
                <p class="museo300"><v-icon color="red">date_range</v-icon>{{ quest.date ? formattedDate(quest.date) : ''}}</p>
              </v-flex>
              <v-flex md6 xs12>
                <v-btn large class="display-1 purple--text text--lighten-1 font-weight-bold" flat><v-icon left>monetization_on</v-icon><p style="line-height:1px" class="museo700">{{ quest.cost }}</p></v-btn>
              </v-flex>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import format from 'date-fns/format'
import axios from 'axios'

  export default {
    computed:{
      quests_sorted(){
        return this.quests.sort((a,b)=>{return a.completed || this.get_date().getTime() > a.date.getTime() ? 1: -1 })
      }
    },
    methods:{
      formattedDate(arg){
        return format(arg, 'D.MM.YYYY')
      },
      get_date(){
        var date = new Date()
        date = new Date(date.getYear() + 1900, date.getMonth(), date.getDate())
        return date
      },
    },
    created(){
      const filter_params = {
        filter: 'quests,info,departments'
      }
      axios.get('https://ocheredsut.ru/api/1/account/', {params: filter_params}).then((user)=>{
        const data = {
          faculty: user.data.info.faculty,
          departments: user.data.departments.join(',')
        }
        axios.get('https://ocheredsut.ru/api/1/quests/', {params: data}).then((quests)=>{
          var temp = quests.data
          for (var quest of temp) {
            var date = new Date()
            var count = null

            if (quest.daily){
              var date = new Date()
              count = user.data.quests.find(a=>{
                return a.id === quest.id && this.formattedDate(a.added * 1000) === format(date, 'D.MM.YYYY')
            })
            }
            else{
              count = user.data.quests.find(a=>{return a.id === quest.id})
            }

            quest.counting.current = count ? count.count.current : 0
            quest.date = new Date(quest.date*1000)
            quest.date.setDate(quest.date.getDate());
            quest.completed = count ? count.completed : false
          }
          this.quests = temp
        })
      })
    },
    data(){
      return {
        quests: []
      }
    }
  }
</script>

<style>
</style>
