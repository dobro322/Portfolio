<template>
  <v-dialog max-width="500px" v-model="show">
    <v-card class="rounded">
      <v-card-title style="font-size: 30px"><p class="text-xs-center">{{ header.name }}</p></v-card-title>
      <v-card-text class="text-xs-center headline">
        <p>{{text}}</p>
      </v-card-text>
      <v-card-actions>
        <v-layout justify-space-between row wrap>
          <v-flex xs6><v-btn block large @click="func(header); show=false" color="green" flat><p>Да</p></v-btn></v-flex>
          <v-flex xs6><v-btn block large @click="show = false" color="red" flat><p>Нет</p></v-btn></v-flex>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    methods:{},
    computed:{
      show: {
        get () {
          return this.visible
        },
        set (value) {
          this.$emit('no')
          return value
        }
      }
    },
    props: ['visible','text', 'header', 'func'],
    data(){
      return{
      }
    }
  }
</script>

<style>
</style>
