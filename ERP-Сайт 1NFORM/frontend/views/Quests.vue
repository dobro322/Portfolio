<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12 sm6 offset-sm3 md4 offset-md4>
        <v-card class="rounded">
          <v-layout text-xs-center class="title" row wrap>
            <v-flex style="cursor:pointer" xs12>
              <p v-ripple="{center:true}" @click="route = 'quests'"  :class="'pa-2 ' + (route === 'quests' ? 'selected': '')" style="border-width: 1px">Квесты</p>
            </v-flex>
            <!-- <v-flex style="cursor:pointer" xs6>
              <p v-ripple="{center:true}" @click="route = 'shop'" :class="'pa-2 ' + (route === 'shop' ? 'selected': '')" >Магазин</p>
            </v-flex> -->
          </v-layout>
        </v-card>
      </v-flex>
      <Quest v-if="route === 'quests'"></Quest>
      <Shop v-else></Shop>
    </v-layout>
  </v-container>
</template>

<script>
import Quest from "../components/QuestsPanel.vue"
import Shop from "../components/Shop.vue"

  export default {
    methods:{},
    components:{Quest,Shop},
    data(){
      return {
        route: 'quests',
      }
    }
  }
</script>

<style>

.link {
  text-decoration: none;
  color: rgba(0,0,0,.8)
}

.selected {
  background-color: rgba(200,200,200,.3);
}

</style>
