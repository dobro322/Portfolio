<template>
  <v-app>
    <v-layout>
      <v-flex md4 offset-md4 xs10 offset-xs1 pt-4>
        <v-img src=""></v-img>
        
      </v-flex>
    </v-layout>
    <router-view></router-view>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld'

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data () {
    return {
      //
    }
  }
}
</script>
