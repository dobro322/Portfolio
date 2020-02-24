<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12 sm8 offset-sm2 md4 offset-md4>
        <v-card class="rounded">
          <v-layout text-xs-center class="title" row wrap>
            <v-flex xs6>
              <router-link class="link" :to="'Team'">
                <p v-ripple="{center:true}" @click="route = 'team'"  :class="'pa-2 ' + (route === 'team' ? 'selected': '')" style="border-right:solid; border-width: 0.5px; border-color:rgb(250,250,250);">Информ</p>
              </router-link>
            </v-flex>
            <v-flex :to="'Rating'" xs6>
              <router-link class="link" :to="'Rating'">
                <p v-ripple="{center:true}" @click="route = 'rating'" :class="'pa-2 ' + (route === 'rating' ? 'selected': '')" >Рейтинг</p>
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
  export default {
    methods:{},
    data(){
      return {
        route: '',
      }
    },
    created(){
    }
  }
</script>

<style>

.link {
  text-decoration: none;
  color: rgba(0,0,0,.8)
}

</style>
