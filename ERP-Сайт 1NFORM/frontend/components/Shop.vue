<template>
  <v-container fluid>
    <v-layout text-xs-center wrap row>
      <v-flex d-flex xs12 sm6 md3 lg2 v-for="slot in slots" :key="slot.id">
        <v-card hover style="display: flex; flex-direction: column;" class="rounded ma-1">
          <v-img max-height="300px" :src="slot.img">
          </v-img>
          <v-card-title class="headline justify-center">
            <p class="museo700">{{slot.title}}</p>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="grow">
            <v-layout column wrap>
              <v-flex xs12 class="font-weight-regular">
                <p>{{ slot.text }}</p>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions>
            <v-layout align-center row wrap>
              <v-flex xs12>
                <v-btn large class="display-1 purple--text text--lighten-1 font-weight-bold" flat><v-icon left>monetization_on</v-icon> ??? </v-btn>
              </v-flex>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

  export default {
    methods:{},
    created(){
      axios.get('https://ocheredsut.ru/api/1/shop/').then((resp)=>{
        this.slots = resp.data
      })
    },
    data(){
      return{
        slots: [
          {
            title: "Носки 1NFORM",
            text: "Теперь дырки будут оправданы логотипом информа",
            img: "https://shop.bowandtie.ru/image/cache/data/foto/noski-baboon/Noski-v-beluyu-i-krasnuyu-polosku-BAB-S-36-1000x1200.jpg",
          }
        ]
      }
    }
  }
</script>

<style>

</style>
