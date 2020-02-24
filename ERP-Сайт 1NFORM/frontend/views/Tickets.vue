<template>
  <v-container fluid>

    <v-dialog v-model="dialog.visible" max-width="500px">
      <v-card>
        <v-card-title class="headline">
          <p>{{dialog.abit.name}}, {{dialog.abit.faculty}}</p>
        </v-card-title>
        <v-card-text>
          <v-layout v-if="dialog.abit.agreement && !dialog.abit.adult" row wrap>
            <v-flex text-xs-center xs12 sm6 offset-sm3>
              <v-img max-height="300px" max-width="auto" :src="dialog.abit.agreement"></v-img>
              <p class="pt-1">Согласие от родителей</p>

              <v-dialog max-width="680px">
                <v-btn slot="activator" color="orange" dark round><p>Открыть фулл</p></v-btn>
                <v-card>
                  <v-img :src="dialog.abit.agreement"></v-img>
                </v-card>
              </v-dialog>

            </v-flex>
          </v-layout>
          <v-layout v-else row wrap>
            <v-flex v-if="dialog.abit.adult">
              <p>Есть 18</p>
            </v-flex>
            <v-flex v-else>
              <p>Согласие отсутствует</p>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-layout text-xs-center row wrap>
            <v-flex v-if="dialog.abit.status === 'checking_age' && dialog.abit.agreement" xs12>
              <v-layout row wrap>
                <v-flex xs6>
                  <v-btn dark color="green" block @click="confirm_agreement"><p>Подтвердить соглашение</p></v-btn>
                </v-flex>
                <v-flex xs6>
                  <v-btn dark block color="orange" @click="dialog.comment.visible = true"><p>Некорректно</p></v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
             <v-flex v-if="dialog.abit.status === 'waiting_for_pay' && (dialog.abit.faculty === check_faculty() || check_role() === '794')">
              <v-layout row wrap>
                <v-flex xs6>
                  <v-btn dark color="green" block @click="confirm_payment"><p>Подтвердить оплату</p></v-btn>
                </v-flex>
                <v-flex xs6>
                  <v-btn dark block color="orange" @click="dialog.comment.visible = true"><p>Некорректно</p></v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex v-if="dialog.comment.visible">
              <v-text-field
                label="Комментарий"
                v-model="dialog.comment.text"
                append-icon="confirm"
              ></v-text-field>
              <v-btn @click="decline"><p>Отправить</p></v-btn>
            </v-flex>
            <v-flex pt-4 xs12>
              <v-btn block class="elevation-2" @click="dialog.visible = false" round flat><p>Закрыть</p></v-btn>
            </v-flex>
          </v-layout>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <v-layout v-if="check_role() >= '724'" justify-space-around column wrap>
      <v-layout row wrap>
        <v-flex order-xs2 order-md1 md6 xs12>
          <v-layout align-center row>
            <v-text-field
              v-model="search"
              label="Поиск"
              color="orange"
              hint="Поиск работает только по всем факультетам"
            ></v-text-field>
            <v-icon @click="search = ''" color="red">close</v-icon>
          </v-layout>
        </v-flex>
        <v-flex  order-xs1 order-md2 md6 xs12>
          <v-layout justify-end row wrap>
            <p class="pr-2" style="font-size:13px"><span class="success dot"></span> - Оплатил</p>
            <p class="pr-2" style="font-size:13px"><span class="primary dot"></span> - Оплачивает</p>
            <p class="pr-2" style="font-size:13px"><span style="background-color:#ecf0f1" class="dot"></span> - Ожидается согласие</p>
            <p class="pr-2" style="font-size:13px"><span class="warning dot"></span> - Требует проверки</p>
            <p class="pr-2" style="font-size:13px"><span style="background-color:#2c3e50" class="dot"></span> - В очереди</p>
            <p class="pr-2" style="font-size:13px"><span style="background-color:#e74c3c" class="dot"></span> - Просрочено</p>
          </v-layout>
        </v-flex>
      </v-layout>
      <v-layout align-center row wrap>
        <v-flex md6>
          <v-card class="elevation-1 rounded">
            <v-layout text-xs-center row wrap>
              <v-flex v-ripple="{center:true}" :class="'Все' === filter ? 'selected': ''" style="cursor:pointer" pa-2 @click="filter = 'Все'">
                <p class="museo700">Все</p>
              </v-flex>
              <v-flex v-ripple="{center:true}" :class="fac.name === filter ? 'selected': ''" :style="'cursor:pointer; border:solid; border-width:0.5px; border-color:rgb(250,250,250);'" pa-2 v-for="fac in faculties" @click="filter = fac.name">
                <p class="museo700">{{fac.name}}</p>
              </v-flex>
            </v-layout>
          </v-card>
        </v-flex>
      </v-layout>
      <v-flex xs12>
        <v-card class="rounded text-xs-center" style="height: 40px">
          <v-layout row wrap>
            <div :style="'color: white; font-size:30px; background:#2ecc71; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'payment_accepted'}).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'payment_accepted'}).length }}</p></div>
            <div :style="'color: white; font-size:30px; background:#3498db; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'waiting_for_pay'}).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'waiting_for_pay'}).length }}</p></div>
            <div :style="'font-size:30px; background:#ecf0f1; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'checking_age'  && a.agreement === '' }).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'checking_age' && a.agreement === '' }).length }}</p></div>
            <div v-if="sorted_participants.filter(a=>{return a.status === 'checking_age' && a.agreement != '' }).length" :style="'color: white; font-size:30px; background:#e67e22; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'checking_age' && a.agreement != '' }).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'checking_age' && a.agreement != '' }).length }}</p></div>
            <div v-if="sorted_participants.filter(a=>{return a.status === 'out_of_tickets'}).length > 0" :style="'color: white; font-size:30px; background:#2c3e50; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'out_of_tickets'}).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'out_of_tickets'}).length }}</p></div>
            <div v-if="sorted_participants.filter(a=>{return a.status === 'out_of_time'}).length > 0" :style="'color: white; font-size:30px; background:#e74c3c; height: 50px; width: ' + (100 * sorted_participants.filter(a=>{return a.status === 'out_of_time'}).length / sorted_participants.length)  + '%' "><p>{{ sorted_participants.filter(a=>{return a.status === 'out_of_time'}).length }}</p></div>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card :style="'border-left:solid; border-width:5px; border-color: ' + color_state(abit)" @click="open_dialog(abit)" hover class="rounded pa-2 ma-1" v-for="abit in sorted_participants">
          <v-layout row wrap>
            <v-flex>
              <p>{{abit.name}}</p>
            </v-flex>
            <v-flex>
              <p>{{abit.faculty}}</p>
            </v-flex>
            <v-flex >
              <p><a target="_blank" :href="'https://vk.com/id' + abit.vkid">Вконтакте</a></p>
            </v-flex>
            <v-flex >
              <p>{{formattedDate(abit.reg_date)}}</p>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout class="display-4" v-else text-xs-center justify-center row wrap>
      <p class="museo900">Сорри, нет прав</p>
    </v-layout>
  </v-container>
</template>
<script>
import format from 'date-fns/format'
import axios from 'axios'

  export default {
    computed: {
      sorted_participants(){
        if(this.search!="") return this.abits.filter(a=>{return a.name.toLowerCase().includes(this.search.toLowerCase())})
        var abits = this.abits.filter(a=>{return this.filter === "Все" ? 1 : a.faculty === this.filter})
        var map = function(a){
          var d = {
            "checking_age": a.agreement === "" ? 3 : 1,
            "waiting_for_pay": 2,
            "payment_accepted": 4,
            "out_of_tickets": 5,
            "out_of_time": 6
          }
          return d[a.status]
        }
        abits = abits.sort((a,b) => { var ta = map(a); var tb = map(b); return ta > tb ? 1 : -1 })
        console.log(abits)
        return abits
      }
    },
    methods: {
        confirm_agreement(){
          const data = {
            status: 1,
            type: 'agreement'
          }
          axios.put('https://ocheredsut.ru/api/1/event/participant/' + this.dialog.abit.vkid, data).then((resp) => {
            this.dialog.visible = false
            this.dialog.abit.status = "waiting_for_pay"
          })
        },
        decline(){
          const data = {
            status: 0,
            type: this.dialog.abit.status === 'checking_age' ? 'agreement' : 'payment',
            msg: this.dialog.comment.text
          }
          axios.put('https://ocheredsut.ru/api/1/event/participant/' + this.dialog.abit.vkid, data).then((resp) => {
            this.dialog.visible = false
          })
        },
        check_faculty(){
          return localStorage.faculty
        },
        confirm_payment(){
          const data = {
            status: 1,
            type: 'payment'
          }
          axios.put('https://ocheredsut.ru/api/1/event/participant/' + this.dialog.abit.vkid, data).then((resp) => {
            this.dialog.visible = false
            this.dialog.abit.status = "payment_accepted"
          })
        },
        color_state(abit){
          if (abit.agreement && abit.status === "checking_age") return "#e67e22"
          if (!abit.agreement && abit.status === "checking_age") return "#ecf0f1"
          if (abit.status === "waiting_for_pay") return "#3498db"
          if (abit.status === "payment_accepted") return "#2ecc71"
          if (abit.status === "out_of_time") return "#e74c3c"
        },
        check_role(){
          return localStorage.role
        },
        formattedDate(arg){
          return format(arg, 'D.MM.YYYY')
        },
        open_dialog(abit){
          this.dialog.abit = abit
          this.dialog.visible = true
        }
     },
    created(){
      axios.get('https://ocheredsut.ru/api/1/event/participants').then((resp) => {
        this.abits = resp.data
        setInterval(()=>{
          axios.get('https://ocheredsut.ru/api/1/event/participants').then((resp)=>{
            this.abits = resp.data
            var t = resp.data.find(a=>{return a.vkid === this.dialog.abit.vkid})
            this.dialog.abit = t ? t : {}
          })
        }, 5000)
      })
    },
    data(){
      return{
        lang: {
            'ИС и Т': 'ИСиТ',
            'ФФП': 'ФП',
            'ИВО': 'ВУЦ'
        },
        abits: [],
        search: "",
        dialog: {
          visible: false,
          abit: {},
          comment: {
            visible: false,
            text: ""
          }
        },
        filter: "Все",
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
        ],
      }
    }
  }
</script>

<style>

</style>
