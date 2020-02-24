<template>
  <v-container fluid>
    <v-layout justify-center row wrap>
      <div>
        <v-card class="rounded">
          <v-layout text-xs-center class="title" row wrap>
            <v-flex  class="all-bordered" style="width:230px" v-for="(dep, index) in departments" :key="index">
              <router-link class="link" :to="'/Kanbanviewer/' + get_path(dep)">
                <p
                  v-ripple="{center:true}"
                  @click="department = get_path(dep)"
                  :class="'pa-2 ' + (department === get_path(dep) ? 'selected ': '')"
                  >{{dep}}
                </p>
              </router-link>
            </v-flex>
          </v-layout>
        </v-card>
      </div>
      <router-view :department="department" :key="department"></router-view>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

  export default {
    methods:{
      get_path(name){
        var dictionary = [
          {
            name: "Все",
            path: "All",
          },
          {
            name: "Фильтрация",
            path: "Filtration",
          },
          {
            name: "Серфинг",
            path: "Surfing",
          },
          {
            name: "Event",
            path: "Event",
          },
          {
            name: "Приемная комиссия",
            path: "PK",
          },
          {
            name: "Собеседники",
            path: "Companions",
          },
          {
            name: "Фандрайзинг",
            path: "Fundraising",
          },
          {
            name: "SMM",
            path: "SMM",
          },
        ]
        return dictionary.find(a=>{return a.name === name}).path
      },
    },
    created(){
      axios.get('https://ocheredsut.ru/api/1/kanban/').then((resp) => {
        this.departments = this.departments.concat(resp.data)

      })
      this.department = this.$route.params.dep
    },
    data(){
      return {
        departments: [],
        department: '',
      }
    }
  }
</script>

<style>

.all-bordered{
  border-style: solid;
  border-width: 0.5px;
  border-color:rgb(250,250,250);
}


</style>
