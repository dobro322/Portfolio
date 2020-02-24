<template>
  <v-app>
    <v-form ref="vkform">
      <v-layout row wrap>
        <v-layout class="headline" hidden-xs-only row wrap>
          <v-flex xs12 sm5><p>ФИО</p></v-flex>
          <v-flex xs12 sm2><p>Дата рождения</p></v-flex>
          <v-flex xs12 sm2><p>Факультет</p></v-flex>
          <v-flex xs12 sm3><p>Вк</p></v-flex>
        </v-layout>
        <v-flex xs12 v-for="abit in abit_array" :key="abit.id">
          <v-card hover :class="'mb-2 rounded ' + (abit.added_conf ? 'check' : (abit.status.name === '4' ? 'cross' :''))" :style="'border-left:solid; border-width:10px; border-color:' + state_color(abit.status.name)">
            <v-layout pa-2 @click="get_abiturient_info(abit)" class="" row wrap>
              <v-flex xs6 :class="$vuetify.breakpoint.xs ? '' : 'title'" sm5><p> <br class="hidden-sm-and-up"> {{abit.full_name}}</p></v-flex>
              <v-flex v-if="abit.status.name !='1'" xs4 :class="$vuetify.breakpoint.xs ? '' : 'title'" sm2><p>{{abit.bdate}}</p></v-flex>
              <v-flex v-else xs4 :class="$vuetify.breakpoint.xs ? '' : 'title'" sm2><p>-</p></v-flex>
              <v-flex xs2 :class="$vuetify.breakpoint.xs ? '' : 'title'" sm2><p>{{abit.faculty}}</p></v-flex>
              <v-flex xs12 :class="$vuetify.breakpoint.xs ? '' : 'title'" sm3><p v-if="abit.vk"><a target="_blank" :href="'https://vk.com/id' + abit.vk">vk.com/id{{abit.vk}}</a></p></v-flex>
              <v-tooltip style="position:absolute; top: 0px; left: 5px" v-if="abit.predictings.length > 0" bottom>
                <v-icon  slot="activator" class="noselect" color="purple lighten-2">visibility</v-icon>
                <span>Помощь системы</span>
              </v-tooltip>
            </v-layout>
            <v-layout style="cursor:default; background-color: rgb(251,251,251)"  v-if="abit.info" row wrap>
              <v-flex lg4 offset-lg4 md6 offset-md3 sm8 offset-sm2 xs12 v-if="abit.status.name==='4' && check_faculty() === abit.faculty">
                <v-btn color="green" @click="adding_conf(abit)" round dark block><p>Я добавлю</p></v-btn>
              </v-flex>
              <v-layout row wrap>
                <v-flex xs12 v-if="predictable(abit) && abit.status.name != '1'">
                    <v-layout row wrap>
                      <v-flex xs12 text-xs-center><p>Есть предложение от системы</p></v-flex>
                      <v-flex lg4 offset-lg4 md6 offset-md3 sm8 offset-sm2 xs12><v-btn dark color="#5f27cd" block round @click="$emit('predict_open', abit)"><p>Открыть</p></v-btn></v-flex>
                    </v-layout>
                </v-flex>
                <v-flex>
                  <v-layout mx-4 justify-space-around row wrap>
                    <v-flex xs12>
                      <v-layout v-if="abit.status.name != '4'" align-center wrap row>
                        <v-flex v-if="abit.status.name === '1'" xs12>
                          <v-btn class="elevation-2" round @click="$emit('take_abit', abit)" color="orange" text-xs-center flat block><p>Берусь</p></v-btn>
                        </v-flex>
                        <v-flex v-if="abit.status.name!='1' && (abit.status.name === '3' || abit.status.taken_by.name == check_name())" xs12>
                          <v-btn v-show="!abit.founded" class="elevation-2" round color="green" @click="abit.founded = true" flat block><p>Нашел</p></v-btn>
                        </v-flex>
                        <v-flex v-if="abit.founded">
                          <v-layout row wrap>
                            <v-flex xs12>
                              <v-text-field
                              :rules="[rules.required, rules.vk]"
                              name="name"
                              label="Вконтакте"
                              v-model="abit.vk"
                              color="orange"
                              ></v-text-field>
                            </v-flex>
                            <v-flex xs6>
                              <v-btn class="elevation-2" round block flat color="green" @click="confirm_vk(abit)"><p>Подтвердить</p></v-btn>
                            </v-flex>
                            <v-flex xs6>
                              <v-btn class="elevation-2" round block flat color="red" @click="abit.founded = false"><p>Отменить</p></v-btn>
                            </v-flex>
                          </v-layout>
                        </v-flex>
                        <v-flex v-if="abit.status.name==='2' && check_name() === abit.status.taken_by.name" xs12>
                          <v-btn class="elevation-2" round color="black" @click="hard_abit(abit)" flat block><p>Сложный</p></v-btn>
                        </v-flex>
                        <v-flex xs12>
                          <v-btn class="elevation-2" round block flat color="green" @click="$emit('comment_abit', abit)"><p>Комментарии ({{abit.comments.length}})</p></v-btn>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-layout>
          </v-card>
        </v-flex>
      </v-layout>
    </v-form>
  </v-app>
</template>
<script>
import axios from 'axios'

export default {
  methods:{
    predictable(abit){
      if(abit.status.name === '4') return false
      if(abit.status.name === '2' && abit.status.taken_by.name != this.check_name()) return false
      for (var i = 0; i < abit.predictings.length; i++) {
        if(!abit.predictings[i].failed)  return true
      }
      return false
    },
    check_faculty(){
      return localStorage.faculty
    },
    adding_conf(abit){
      this.$emit('adding_conf', abit)
    },
    get_abiturient_info(abit){
      if(!abit.info){
          const data = {
            filter: "comments,pic,vk,status"
          }
          axios.get('https://ocheredsut.ru/api/1/abits/' + abit.id, {params: data}).then((resp)=>{
            abit.comments = resp.data.comments
            abit.pic = resp.data.pic
            abit.vk = resp.data.vk
            abit.status = resp.data.status
            abit.info = true
          })
      }
      else{
        abit.info = false
      }
    },
    check_name(){
      return localStorage.name
    },
    confirm_vk(abit){
      if(this.$refs.vkform.validate()){
        this.$emit('confirm_vk', abit)
      }
    },

    hard_abit(abit){
      this.$emit('hard_abit', abit)
    },

    state_color(arg){
      const states = {
        '4':'#2ecc71',
        '1':'#ecf0f1',
        '3':'#2c3e50',
        '2':'#e67e22'
      }
      return states[arg]
    },
  },
  computed:{
    abit_array(){
      return this.abits
    }
  },
  props: ['abits','filter','max_value'],
  data(){
    return{
      abit_filter: this.filter,
      rules: {
        required: value => !!value.replace(/\s+/, "") || 'Обязательное поле',
        min: v => v.length >= 8 || 'Минимум 8 букв',
        vk: v => v.match(/((https?:[/]{2})?(m.)?vk.com[/].+)/i) ? true: false || 'Обязателен формат vk.com'
      },
    }
  }
}
</script>

<style>

</style>
