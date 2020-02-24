<template>
  <v-app>
    <v-container fluid>
      <v-layout :class="$vuetify.breakpoint.xs ? 'display-1' : 'display-4'" text-xs-center justify-center align-center row wrap>
        <p>Добро пожаловать</p>
        <p>Главная страница в разработке 🌚</p>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
  export default {
    methods:{},
    data(){
      return {
        routes: [
          {
            name: "Новости",
            path: "/News",
          },
          {
            name: "Рейтинг",
            path: "/Rating",
          },
          {
            name: "Квесты",
            path: "/Quests",
          },
          {
            name: "Магазин",
            path: "/Shop",
          },
        ]
      }
    }
  }
</script>

<style>
</style>
