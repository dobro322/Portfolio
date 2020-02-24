<template>
  <v-form ref="vkform">
  <v-layout row wrap>
    <v-flex xs12 md3 sm4 lg2 pa-2 v-for="abit in abit_array" :key="abit.id">
      <v-card
      :style="'border-top: solid;border-width:15px; border-color:' + state_color(abit.status.name)"
      min-height = "200px"
      :class="'rounded ma-1 ' + (abit.added_conf ? 'check' : (abit.status.name === '4' ? 'cross' :''))"
      >
        <v-card-title class="headline">
          <v-tooltip v-if="abit.predictings.length > 0" bottom>
            <v-icon style="position:absolute; top: 0px; left: 5px" slot="activator" class="noselect" color="purple lighten-2">visibility</v-icon>
            <span>Помощь системы</span>
          </v-tooltip>
          <v-tooltip bottom>
            <v-icon style="position:absolute; top: 5px; right: 5px" slot="activator" class="noselect" color="grey" @click="$copyText(abit.full_name)" :v-ripple="{center:true}">assignment</v-icon>
            <span>Скопировать</span>
          </v-tooltip>
          <v-layout row wrap>
            <v-flex xs12><p>
              {{ abit.full_name }}
            </p><p v-if="abit.status.name != '1'" class="museo300" style="font-size:20px">{{ abit.bdate }}</p><p class="museo300" style="font-size:20px">{{ abit.faculty }}</p><p class="museo300" style="font-size:20px">{{ abit.specialization.split(" ")[0] }}</p></v-flex>
            <v-flex xs12>
              <v-btn color="purple" block flat round @click="get_abiturient_info(abit)"><v-icon>{{ abit.info ? 'keyboard_arrow_up' : 'keyboard_arrow_down'}}</v-icon> </v-btn>
            </v-flex>
          </v-layout>
        </v-card-title>
        <v-slide-y-transition>
        <v-card-text v-if="abit.info" style="padding-top: 0">
          <v-flex v-if="abit.status.name==='4' && check_faculty() === abit.faculty && !abit.status.adding_by" xs12 >
            <v-btn color="green" @click="adding_conf(abit)" round dark block><p>Я добавлю</p></v-btn>
          </v-flex>
            <div v-if="predictable(abit) && abit.status.name != '1'">
              <v-layout row wrap>
                <v-flex xs12 text-xs-center><p>Есть предложение от системы</p></v-flex>
                <v-flex><v-btn dark color="#5f27cd" round block class="elevation-1" @click="$emit('predict_open', abit)"><p>Открыть</p></v-btn></v-flex>
              </v-layout>
            </div>
            <div>
              <v-layout mt-1 text-xs-center row  wrap v-if="abit.info && abit.pic">
                <v-flex>
                  <v-avatar size="150">
                    <v-img max-height="150" :src="abit.pic"></v-img>
                    <a :href="'https://vk.com/id' + abit.vk" target="_blank" style="text-decoration:none; position: absolute; top:105px; left:105px"><img style="height:40px"src="https://1.bp.blogspot.com/-2jQQ7FrGtGU/XFsqyrZRIwI/AAAAAAAAH3Y/UZ_DqDQeCdM9aTZKyE2gStTAn3Je3jNbACK4BGAYYCw/s1600/logo%2Bvk.png"></img></a>
                  </v-avatar>
                </v-flex>
              </v-layout>
            <v-layout v-if="abit.status.name != '4'" wrap row>
                <v-flex v-if="abit.status.name === '1'" xs12>
                  <v-btn @click="$emit('take_abit', abit)" color="orange" text-xs-center flat block><p>Берусь</p></v-btn>
                </v-flex>
                <v-flex v-if="abit.status.name!='1' && (abit.status.name === '3' || abit.status.taken_by.name == check_name())" xs12>
                  <v-btn color="green" @click="abit.founded = true" flat block><p>Нашел</p></v-btn>
                </v-flex>
                  <v-flex v-if="abit.founded">
                      <v-layout row wrap>
                        <v-flex xs12>
                          <v-text-field
                            :rules="[rules.vk]"
                            name="name"
                            label="Вконтакте"
                            v-model="abit.vk"
                            color="orange"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs6>
                          <v-btn block flat color="green" @click="confirm_vk(abit)"><p>Подтвердить</p></v-btn>
                        </v-flex>
                        <v-flex xs6>
                          <v-btn block flat color="red" @click="abit.founded = false"><p>Отменить</p></v-btn>
                        </v-flex>
                      </v-layout>
                  </v-flex>
                <v-flex v-if="abit.status.name==='2' && check_name() === abit.status.taken_by.name" xs12>
                  <v-btn color="black" @click="hard_abit(abit)" flat block><p>Сложный</p></v-btn>
                </v-flex>
              </v-layout>
            <v-layout wrap row>
              <v-flex v-if="abit.status.taken_by" pt-4 xs12><p>Кто взялся: <router-link target="_blank" :to="'Companions/team/' + abit.status.taken_by.id">{{ abit.status.taken_by.name }}</router-link></p></v-flex>
              <v-flex v-if="abit.status.date_taken" xs12><p>Когда: {{ formattedDate(abit.status.date_taken) }}</p></v-flex>
              <v-flex v-if="abit.status.found_by" xs12><p>Кто нашел: <router-link target="_blank" :to="'Companions/team/' + abit.status.found_by.id">{{ abit.status.found_by.name }}</router-link></p></v-flex>
              <v-flex v-if="abit.status.date_found" xs12><p>Когда: {{ formattedDate(abit.status.date_found) }}</p></v-flex>
              <v-flex v-if="abit.status.adding_by" xs12><p>Кто добавит <router-link target="_blank" :to="'Companions/team/' + abit.status.adding_by.id">{{ abit.status.adding_by.name }}</router-link></p></v-flex>
              <v-flex>
                <v-btn round block flat color="green" @click="$emit('comment_abit', abit)"><p>Комментарии ({{abit.comments.length}})</p></v-btn>
              </v-flex>
              <v-flex v-if="check_name() === abit.status.found_by.name" pt-2>
                <v-btn round block flat color="red" @click="$emit('drop_abit', abit)"><p>Отменить</p></v-btn>
              </v-flex>
            </v-layout>
            </div>
        </v-card-text>
      </v-slide-y-transition>
      </v-card>
    </v-flex>
  </v-layout>
</v-form>
</template>

<script>
import format from 'date-fns/format'
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
      formattedDate(arg){
        return arg ? format(new Date(arg*1000), 'H:mm D.MM') : ''
      },
      check_name(){
        return localStorage.name
      },
      check_faculty(){
        return localStorage.faculty
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
      confirm_vk(abit){
        if(this.$refs.vkform.validate()){
          this.$emit('confirm_vk', abit)
        }
      },
      adding_conf(abit){
        this.$emit('adding_conf', abit)
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
          vk: v => v.match(/((https?:[/]{2})?(m.)?vk.com[/].+)/i) ? true : false || 'Обязателен формат vk.com'
        },
      }
    }
  }
</script>

<style>

.cross {
  background-image:linear-gradient(rgba(255,255,255,.8),
                   rgba(255,255,255,.8)),
                   url('../assets/img/cross.png');
  background-origin:padding-box;
  background-size: 75px;
  background-clip: padding-box;
  background-position: top right;
}

.check {
  background-image:linear-gradient(rgba(255,255,255,.8),
                   rgba(255,255,255,.8)),
                   url('../assets/img/check.png');
  background-origin:padding-box;
  background-size:75px;
  background-clip: padding-box;
  background-position: top right;
}

</style>
