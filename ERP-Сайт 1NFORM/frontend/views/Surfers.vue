<template>
  <v-container fluid>

    <Comments @delete_comment="delete_comment" :key="AbitComment.title" :header="AbitComment.title" :comments="AbitComment.comments" :visible="AbitComment.dialog" @close="AbitComment.dialog = false" @add_comment="add_comment"></Comments>

    <v-layout align-center row wrap>
      <v-flex order-xs2 order-md1 md6 xs12>
        <v-layout align-center row>
          <v-text-field
            @change="get_abiturients()"
            label="Поиск"
            color="orange"
            hint="Поиск работает только по всем факультетам"
            v-model="search"
          ></v-text-field>
          <v-icon @click="search='', get_abiturients()" color="red">close</v-icon>
        </v-layout>
      </v-flex>
      <v-flex order-xs1 order-md2 md6 xs12>
        <v-layout justify-end row wrap>
          <p class="pr-2" style="font-size:13px"><span style="background-color:#ecf0f1" class="dot"></span> - Свободный</p>
          <p class="pr-2" style="font-size:13px"><span class="warning dot"></span> - Сёрфят</p>
          <p class="pr-2" style="font-size:13px"><span class="secondary dot"></span> - Не нашли</p>
          <p class="pr-2" style="font-size:13px"><span class="success dot"></span> - Найден</p>
        </v-layout>
      </v-flex>
    </v-layout>
    <v-layout align-center row wrap>
      <v-flex md6>
        <v-card class="elevation-1 rounded">
          <v-layout text-xs-center row wrap>
            <v-flex v-ripple="{center:true}" :class="'Все' === filter ? 'selected': ''" style="cursor:pointer" pa-2 @click="filter = 'Все'; sorted_abits = 1">
              <p class="museo700">Все</p>
            </v-flex>
            <v-flex v-ripple="{center:true}" :class="fac.name === filter ? 'selected': ''" :style="'cursor:pointer; border:solid; border-width:0.5px; border-color:rgb(250,250,250);'" pa-2 v-for="fac in faculties" @click="filter = fac.name; sorted_abits = 1">
              <p class="museo700">{{fac.name}}</p>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout pt-2 align-center  row wrap>
      <v-flex xs12 sm12 md5 lg6>
        <v-card class="elevation-1 rounded">
          <v-layout  text-xs-center row wrap>
            <v-flex v-ripple="{center:true}" :class="state.state === status_filter ? 'selected': ''" :style="'cursor:pointer; border:solid; border-width:0.5px; border-color:rgb(250,250,250)'" pa-2 v-for="state in filtered_states" @click="status_filter = state.state; sorted_abits = 1">
              <p class="museo700">{{state.name}}</p>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout pt-2 align-center  row wrap>
      <v-flex xs12 sm12 md2 lg3>
        <v-card class="elevation-1 rounded">
          <v-layout  text-xs-center row wrap>
            <v-flex v-ripple="{center:true}" :class="mine  ? '' : 'selected'" :style="'cursor:pointer; border:solid; border-width:0.5px; border-color:rgb(250,250,250)'" pa-2 @click="mine = false; sorted_abits = 1">
              <p class="museo700">Все</p>
            </v-flex>
            <v-flex v-ripple="{center:true}" :class="mine  ? 'selected' : ''" :style="'cursor:pointer; border:solid; border-width:0.5px; border-color:rgb(250,250,250)'" pa-2 @click="mine = true; sorted_abits = 1">
              <p class="museo700">Мои</p>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>


    <Predictings @close="predict_dialog.visible = false" @failed="fail_predict" @success="success_predict" :visible="predict_dialog.visible" :abit="predict_dialog.abit"></Predictings>
    <YNPanel :func="ynpanel.function" @no="ynpanel.visible = false" :visible="ynpanel.visible" :header="ynpanel.header" :text="ynpanel.text"></YNPanel>

    <v-layout align-center justify-space-between row wrap>
      <v-flex xs12><div class="display-1"><p>{{ search ? 'Все' : filter }}</p></div></v-flex>
      <div class="display-1"><p>Всего {{ founded }} из {{ max }}</p></div>
      <div>
        <v-layout row wrap>
          <v-icon class="noselect" @click="panels = !panels" large>{{ panels ? 'view_stream' : 'view_column'}}</v-icon>
        </v-layout>
      </div>
    </v-layout>

    <PanelSurf v-if="panels"
      :abits="sorted_abits"
      @comment_abit='open_comment'
      @take_abit='take_abit'
      @confirm_vk='confirm_vk'
      @hard_abit='hard_abit'
      @adding_conf='adding_conf'
      @predict_open='open_predict_dialog'
      @drop_abit="drop_abit"
    ></PanelSurf>
    <TableSurf v-else
      :abits="sorted_abits"
      @comment_abit='open_comment'
      @take_abit='take_abit'
      @confirm_vk='confirm_vk'
      @adding_conf='adding_conf'
      @hard_abit='hard_abit'
      @predict_open='open_predict_dialog'
    ></TableSurf>
    <v-layout row wrap>
      <v-btn flat block color="green" @click="max_value+=25;get_abiturients()" prepend-icon> <v-icon>plus</v-icon>Показать больше</v-btn>
    </v-layout>
  </v-container>
</template>

<script>
import PanelSurf from '../components/PanelSurf.vue'
import Comments from '../components/Comments.vue'
import YNPanel from '../components/YNPanel.vue'
import TableSurf from '../components/TableSurf.vue'
import Predictings from '../components/Predictings.vue'
import axios from 'axios'


  export default {
    components: {PanelSurf,Comments,YNPanel,TableSurf,Predictings},
    computed: {
      filtered_states(){
        return this.states.filter(a=>{return (this.mine ? !"Свободные".includes(a.name) : 1 )})
      },
      count(){
          return {
            max: this.abiturients.length,
            count: this.abiturients.filter(a=>{return a.status.name === '4'}).length
        }
      },
      nowtime(){
        return new Date()
      },
      sorted_abits: {
        set(){
          this.max_value = 25
          this.get_abiturients()
        },
        get(){
          return this.abiturients
        }
      }
    },
    created(){
      const data = {
        faculties: this.filter,
        status: this.status_filter,
        personal: this.mine,
        search: this.search,
        fields: "id,full_name,faculty,bdate,status,added_conf,predictings,vk,specialization",
        limit: this.max_value
      }
      axios.get('https://ocheredsut.ru/api/1/abits/', {params: data}).then((resp)=>{
        this.abiturients = resp.data.data.map(a=>{
          a.info = false;
          a.founded = false;
          return a
        })
        this.max = resp.data.max
        this.founded = resp.data.founded
      })
      setInterval(a=>{
        this.get_abiturients()
      }, 10000)
    },
    data(){
      return {
        predict_dialog: {
          abit: {
            full_name: '',
            predictings: []
          },
          visible: false
        },
        status_filter: "Все",
        max_value: 25,
        panels: this.$vuetify.breakpoint.xs ? false : true,
        filter: 'Все',
        rules: {
          required: value => !!value.replace(/\s+/, "") || 'Обязательное поле',
          min: v => v.length >= 8 || 'Минимум 8 букв'
        },
        AbitComment: {
          title: '',
          comments: {},
          dialog: false
        },
        ynpanel: {
          visible: false,
          header: '',
          text: ''
        },
        search: null,
        max: 0,
        founded: 0,
        faculties: [
          {
            name: "ИКСС",
            color: "rgba(255, 159, 67, 1)",
          },
          {
            name: "ИСиТ",
            color: "rgba(95, 39, 205,1)",
          },
          {
            name: "РТС",
            color: "rgba(238, 82, 83,1)",
          },
          {
            name: "ГФ",
            color: "rgba(254, 202, 87,1)",
          },
          {
            name: "ВУЦ",
            color: "rgba(16, 172, 132,1)",
          },
          {
            name: "ЦЭУБИ",
            color: "rgba(84, 160, 255,1)",
          },
          {
            name: "ФП",
            color: "rgba(34, 47, 62,1)",
          },
          {
            name: "ИНО",
            color: "rgba(0, 210, 211,1)",
          },
          {
            name: "СПбКТ",
            color: "rgba(10, 189, 227,1)",
          },
        ],
        abiturients: [],
        mine: false,
        states: [
          {
            name: "Все",
            state: "Все"
          },
          {
            name: "Свободные",
            state: "1"
          },
          {
            name: "Занятые",
            state: "2"
          },
          {
            name: "Сложные",
            state: "3"
          },
          {
            name: "Найденные",
            state: "4"
          }
        ]
      }
    },
    methods:{
      adding_conf(abit){
        this.ynpanel = {
          header: abit,
          visible: true,
          text: 'Добавите в конфу?'
        }
        this.ynpanel.function = (abit => {
          const data = {
            type: "adding_conf",
          }
          axios.put('https://ocheredsut.ru/api/1/abits/'+abit.id, data).then((resp)=> {
            abit.status = resp.data.status
          })
        })
      },
      fail_predict(predict){
        const data = {
          type: 'predict_failed',
          predict_vk: predict.id
        }
        axios.put("https://ocheredsut.ru/api/1/abits/" + this.predict_dialog.abit.id, data).then((resp)=>{
          this.predict_dialog.abit.predictings = resp.data.predictings
        })
      },
      success_predict(predict){
        const data = {
          type: 'predict_success',
          predict_vk: predict.id
        }
        axios.put("https://ocheredsut.ru/api/1/abits/" + this.predict_dialog.abit.id, data).then((resp)=>{
          this.predict_dialog.abit.status = resp.data.status
          this.predict_dialog.visible = false

        })
      },
      open_predict_dialog(abit){
        this.predict_dialog = {
          abit: abit,
          visible: true
        }
      },
      get_abiturients(){
        const data = {
          faculties: this.filter,
          status: this.status_filter,
          personal: this.mine,
          search: this.search,
          fields: "id,full_name,faculty,bdate,status,added_conf,predictings,vk,specialization",
          limit: this.max_value
        }
        axios.get('https://ocheredsut.ru/api/1/abits/', {params: data}).then((resp)=>{
          var temp = resp.data.data
          for(var i = 0; i < temp.length; i++){
            var ind = this.abiturients.findIndex(a=>{return a.id === temp[i].id})
            if(ind >= 0){
              temp[i].founded = this.abiturients[ind].founded;
              temp[i].info = this.abiturients[ind].info;
              if(temp[i].info){
                temp[i].comments = this.abiturients[ind].comments;
                temp[i].pic = this.abiturients[ind].pic;
              }
            }
            else{
              temp[i].founded = false;
              temp[i].info = false;
            }
          }
          this.max = resp.data.max
          this.founded = resp.data.founded
          this.abiturients = temp
        })
      },
      hard_abit(arg){
        this.ynpanel = {
          header: arg,
          visible: true,
          text: 'Сложновато, да?'
        }
        this.ynpanel.function = (arg => {
          const data = {
            type: "hard_abit",
          }
          axios.put('https://ocheredsut.ru/api/1/abits/'+arg.id, data).then((resp)=> {
            arg.status = resp.data.status
          })
        })
      },
      take_abit(arg){
        this.ynpanel = {
          header: arg,
          visible: true,
          text: 'Беретесь за поиск?'
        }
        this.ynpanel.function = (arg => {
          const data = {
            type: "take_abit",
          }
          axios.put('https://ocheredsut.ru/api/1/abits/'+arg.id, data).then((resp)=> {
            arg.status = resp.data.status
          })
        })
      },
      confirm_vk(arg){
        this.ynpanel = {
          header: arg,
          visible: true,
          text: 'Подтверждаете ' + arg.vk.replace('https://', '') + '?'
        }
        this.ynpanel.function = (arg => {
          const data = {
            type: "confirm_abit",
            vk: arg.vk
          }
          axios.put('https://ocheredsut.ru/api/1/abits/'+arg.id, data).then((resp)=> {
            arg.status = resp.data.status
            arg.vk = resp.data.vk
            arg.pic = resp.data.pic
            arg.founded = false;
          })
        })
      },
      drop_abit(arg){
        this.ynpanel = {
          header: arg,
          visible: true,
          text: 'Сбросить ' + arg.full_name
        }
        this.ynpanel.function = (arg => {
          const data = {
            type: "drop",
            vk: arg.vk
          }
          axios.put('https://ocheredsut.ru/api/1/abits/'+arg.id, data).then((resp)=> {
            arg.status = resp.data.status
            arg.vk = resp.data.vk
            arg.pic = resp.data.pic
            arg.founded = false;
          })
        })
      },
      open_comment(arg){
        arg.name = arg.full
        this.AbitComment.comments = arg.comments
        this.AbitComment.title = arg.full_name
        this.AbitComment.abit_id = arg.id
        this.AbitComment.dialog = true
      },
      add_comment(arg){
        const data = {
          type: "comment",
          comment: arg
        }
        axios.put('https://ocheredsut.ru/api/1/abits/'+this.AbitComment.abit_id, data).then((resp)=> {
          this.AbitComment.comments = resp.data.comments
        })

      },
      delete_comment(arg){
        const data = {
          comment: arg
        }
        axios.post('https://ocheredsut.ru/api/1/abits/'+this.AbitComment.abit_id+'/comments', data).then((resp)=> {
          this.AbitComment.comments = resp.data.comments
        })

      },
    }
  }
</script>

<style>

.v-input__icon--append .v-icon {
    color: orange;
}

.v-input__icon--append-outer .v-icon {
    color: red;
}

.dot {
  height: 12px;
  width: 12px;
  border-radius: 50%;
  display: inline-block;
}

.selected{
  background-color: rgba(52, 73, 94,1.0);
  color:white;
}
</style>
