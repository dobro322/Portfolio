<template>
  <v-content v-if="visible">
    <v-container fill-height>
      <v-layout justify-center align-center row wrap>
        <div><a style="text-decoration: none" href="https://oauth.vk.com/authorize?client_id=6630817&display=page&redirect_uri=https://1nform.ru/logging&scope=offline&response_type=code&v=5.101&state=123456"><v-btn dark color="green" large><p>Залогиниться</p></v-btn></a></div>
      </v-layout>
    </v-container>
  </v-content>
</template>
<script>
import axios from 'axios'
import format from 'date-fns/format'
  export default {
    props: ["visible"],
    methods: { },
    sended: false,
    data(){
      return{}
    },
    created(){

      if(this.$route.query.code && !this.sended){
        const data = {
          code: this.$route.query.code
        }
        this.sended = true
        this.$emit('code', data)

      }
    }
}
</script>

<style>

#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

.file-btn{
  cursor: pointer;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  z-index: 10;
  cursor: pointer;
}

#preview img {
  max-height: 400px;
  max-width: 300px;
}
</style>
