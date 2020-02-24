<template>
  <v-layout justify-center>
    <v-dialog persistent scrollable max-width="400px" v-model="show">
    <v-form ref="form">
      <v-card style="background-color:white"  class="rounded">
        <v-card-title class="title"><p>Комментарии для <br> "{{ header }}"</p></v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0" style="height: 300px;">
          <div class="px-2" style="border-bottom: solid; border-width: 0.5px; border-color:rgba(150,150,150,0.5)"  v-for="comm in comments">
            <div v-if="check_name() === comm.author" style="display: flex; margin-right: 20px; float: right; width: 10px"> <v-btn @click="$emit('delete_comment', comm)" flat small icon color="red"> <v-icon small>close</v-icon> </v-btn> </div>
            <v-layout pt-2 row wrap>
              <v-flex hidden-sm-and-down md2>
                <v-avatar size="50">
                  <v-img :src="comm.pic"></v-img>
                </v-avatar>
              </v-flex>
              <v-flex md10>
                <v-layout row wrap>
                  <v-flex xs12  class="orange--text text--darken-4"><p>{{comm.author.split(' ')[0]}} {{comm.author.split(' ')[1]}}<span class="pl-2 museo500" style="color:rgb(150,150,150); font-size:12px;">{{formattedDate(comm.date)}}</span></p></v-flex>
                  <v-flex xs12 class="subheading"><p>{{comm.text}}</p></v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-layout align-center row wrap>
            <v-flex px-4 xs12>
              <v-textarea
                outline
                height="80px"
                validate-on-blur
                autofocus
                color="orange"
                :rules="[rules.required]"
                v-model = "text"
                label = "Ваш комментарий"
              ></v-textarea>
            </v-flex>
            <v-flex xs6><v-btn round block color="orange darken-4" flat @click="add_comment"><p>Отправить</p></v-btn></v-flex>
            <v-flex xs6><v-btn round block flat @click="show = false"><p>Закрыть</p></v-btn></v-flex>
          </v-layout>
        </v-card-actions>
      </v-card>
    </v-form>
    </v-dialog>
  </v-layout>
</template>

<script>
import format from 'date-fns/format'

  export default {
    methods:{
      add_comment(){
        if(this.$refs.form.validate()){
          this.$emit('add_comment', this.text)
          this.text = ''
          this.$refs.form.resetValidation()
        }
      },
      formattedDate(arg){
        return arg ? format(new Date(arg*1000), 'H:mm D.MM') : ''
      },
      check_name(){
        return localStorage.name
      },
    },
    computed:{
      show: {
        get () {
          return this.visible
        },
        set (value) {
          this.$emit('close')
          return value
        },
      },
    },
    props: ['comments', 'header', 'visible'],
    data(){
      return{
        rules:{
          required: v => !!(v.replace(/\s+/, "")) || "Обязательное поле!"
        },
        text: '',
        valid: null,
      }
    }
  }
</script>

<style>

</style>
