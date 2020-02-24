<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12 sm8 offset-sm2 md4 offset-md4>
        <v-card class="rounded">
          <v-layout text-xs-center class="title" row wrap>
            <v-flex class="all-bordered" style="width:230px" v-for="(dep, index) in departments" :key="index">
              <router-link class="link" :to="'/Additional/' + get_path(dep)">
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
      </v-flex>
      <router-view></router-view>
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
            name: "Фильтрация",
            path: "Filtration",
          },
          {
            name: "Фандрайзинг",
            path: "Fundraising",
          },
        ]
        return dictionary.find(a=>{return a.name === name}).path
      }
    },
    created(){
      axios.get('https://ocheredsut.ru/api/1/kanban/').then((resp) => {
        if(resp.data.includes("Фильтрация")) this.departments.push("Фильтрация")
        if(resp.data.includes("Фандрайзинг")) this.departments.push("Фандрайзинг")
        this.department = this.departments[0]
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

</style>
