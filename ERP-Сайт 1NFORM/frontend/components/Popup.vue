<template>
  <v-snackbar
    v-model="start"
    color="grey lighten-4"
    top
    vertical
    auto-height
    :timeout="0"
  >
    <p class="orange--text" style="font-size: 18px">{{ text }}</p>
    <v-btn
      color="orange"
      flat
      @click="start = false"
    >
      <v-icon>close</v-icon>
    </v-btn>
  </v-snackbar>
</template>

<script>
  export default {
    methods:{},
    props: ['text','open'],
    data(){
      return{
        start: this.open
      }
    }
  }
</script>

<style>
@font-face {
	font-family: "Museo";
	src: url('../assets/fonts/MuseoSansCyrl-500.otf');
}

@font-face {
	font-family: "MuseoBold";
	src: url('../assets/fonts/MuseoSansCyrl-700.otf');
}

p {
  font-family: 'Museo';
  line-height: 1.5;
  margin-bottom: 0;
  vertical-align: middle;
}
</style>
