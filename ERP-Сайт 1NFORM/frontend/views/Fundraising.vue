<template>
  <v-container fluid>
    <YNPanel :func="ynpanel.function" @no="ynpanel.visible = false" :visible="ynpanel.visible" :header="ynpanel.header" :text="ynpanel.text"></YNPanel>
    <v-dialog
      v-model="dialog"
      scrollable
      max-width="500px"
    >
      <v-card class="rounded">
        <v-card-title class="headline">
          <p>Новый партнер</p>
        </v-card-title>
        <v-card-text>
          <v-form ref="new_form">
            <v-layout row wrap>

              <v-flex xs12>
                <v-text-field
                  :rules="[rules.required]"
                  label="Наименование компании"
                  prepend-icon="work"
                  v-model="temp_row.name"
                ></v-text-field>
              </v-flex>
              <v-flex sm6 xs12>
                <v-autocomplete
                  label="Статус"
                  :items="states.map(a=>{return a.name})"
                  :color="state_color(temp_row.state)"
                  prepend-icon="check_circle"
                  v-model="temp_row.state"
                ></v-autocomplete>
              </v-flex>
              <v-flex sm6 xs12>
                <v-autocomplete
                  prepend-icon="account_circle"
                  label="Кто общается"
                  v-model="temp_row.operator"
                  :items="operators"
                ></v-autocomplete>
              </v-flex>
              <v-flex sm6 xs12>
                <v-text-field
                  :rules="[rules.required]"
                  label="Сайт"
                  prepend-icon="language"
                  v-model="temp_row.site"
                ></v-text-field>
              </v-flex>
              <v-flex sm6 xs12>
                <v-text-field
                  :rules="[rules.required]"
                  label="Контакты"
                  hint="Почта"
                  prepend-icon="email"
                  v-model="temp_row.contacts"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  :rules="[rules.required]"
                  label="От нас"
                  prepend-icon="card_membership"
                  v-model="temp_row.from_us"
                ></v-textarea>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  :rules="[rules.required]"
                  label="От них"
                  prepend-icon="redeem"
                  v-model="temp_row.from_them"
                ></v-textarea>
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-layout justify-end text-xs-center row wrap>
            <v-flex md3 xs6>
              <v-btn flat color="red" @click="dialog = false"><p>Закрыть</p></v-btn>
            </v-flex>
            <v-flex md3 xs6>
              <v-btn flat @click="add_partner" color="green"><p>Добавить</p></v-btn>
            </v-flex>
          </v-layout>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="edit_dialog"
      scrollable
      max-width="500px"
    >
    <v-card class="rounded">
      <v-card-title class="headline">
        <p>Редактирование</p>
      </v-card-title>
      <v-card-text>
        <v-form ref="edit_form">
          <v-layout row wrap>

            <v-flex xs12>
              <v-text-field
                :rules="[rules.required]"
                label="Наименование компании"
                prepend-icon="work"
                v-model="temp_row.name"
              ></v-text-field>
            </v-flex>
            <v-flex sm6 xs12>
              <v-autocomplete
                label="Статус"
                :items="states.map(a=>{return a.name})"
                :color="state_color(temp_row.state)"
                prepend-icon="check_circle"
                v-model="temp_row.state"
              ></v-autocomplete>
            </v-flex>
            <v-flex sm6 xs12>
              <v-autocomplete
                prepend-icon="account_circle"
                label="Кто общается"
                v-model="temp_row.operator"
                :items="operators"
              ></v-autocomplete>
            </v-flex>
            <v-flex sm6 xs12>
              <v-text-field
                label="Сайт"
                prepend-icon="language"
                v-model="temp_row.site"
              ></v-text-field>
            </v-flex>
            <v-flex sm6 xs12>
              <v-text-field
                :rules="[rules.required]"
                label="Контакты"
                hint="Почта"
                prepend-icon="email"
                v-model="temp_row.contacts"
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-textarea
                :rules="[rules.required]"
                label="От нас"
                prepend-icon="card_membership"
                v-model="temp_row.from_us"
              ></v-textarea>
            </v-flex>
            <v-flex xs12>
              <v-textarea
                :rules="[rules.required]"
                label="От них"
                prepend-icon="redeem"
                v-model="temp_row.from_them"
              ></v-textarea>
            </v-flex>
          </v-layout>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-layout justify-end text-xs-center row wrap>
          <v-flex md3 xs6>
            <v-btn flat color="red" @click="edit_dialog = false"><p>Закрыть</p></v-btn>
          </v-flex>
          <v-flex md3 xs6>
            <v-btn flat @click="edit_partner" color="green"><p>Сохранить</p></v-btn>
          </v-flex>
        </v-layout>
      </v-card-actions>
    </v-card>
    </v-dialog>


    <v-layout row wrap>

      <v-flex>
        <v-layout justify-end row wrap>
            <p style="font-size:15px" class="pr-1"><span style="background-color:#1dd1a1" class="dot"></span> - Спонсор согласился</p>
            <p style="font-size:15px" class="pr-1"><span style="background-color:#ee5253" class="dot"></span> - Отказал</p>
            <p style="font-size:15px" class="pr-1"><span style="background-color:#ff9ff3" class="dot"></span> - Написал</p>
            <p style="font-size:15px"><span style="background-color:#c8d6e5" class="dot"></span> - Не написал</p>
        </v-layout>
      </v-flex>


      <v-flex xs12>
        <v-layout row justify-end wrap>
          <v-flex xs6 md2>
            <v-btn @click="open_partner_dial" prepend-icon flat color="green"><v-icon>add</v-icon>Добавить</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>

      <v-flex hidden-md-and-down xs12>
        <v-layout row wrap>
          <v-flex xs2 class="headline" v-for="col in columns" :key="col"><p>{{ col }}</p></v-flex>
        </v-layout>
        <v-divider></v-divider>
      </v-flex>


      <v-flex xs12 v-for="row in rows" pt-2>
        <v-card class="rounded" flat>
          <v-layout align-center pl-2 py-2 :style="'font-size:15px; border-left:solid; border-width:10px; border-color:' + state_color(row.state)" row wrap>
            <v-flex xs12 md2>
              <v-layout align-center justify-start row wrap>
                  <v-btn v-if="check_role() >= '724'" small icon @click="delete_data(row)" class="red--text"><v-icon>close</v-icon></v-btn>
                  <v-btn small icon @click="open_edit_partner_dial(row)" class="blue--text"><v-icon>edit</v-icon></v-btn>
                  <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px">{{ row.name }}</p>
              </v-layout>
            </v-flex>
            <v-flex xs12 md2>
              <p class="hidden-md-and-up" style="font-family:MuseoBold; font-size:20px">Сайт</p>
              <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px"><a target="_blank" style="text-decoration:none" :href="row.site">{{ row.site }}</a></p>
            </v-flex>
            <v-flex xs12 md2>
              <p class="hidden-md-and-up" style="font-family:MuseoBold; font-size:20px">Контакты</p>
              <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px"><a target="_blank"  style="text-decoration:none" :href="row.contacts.includes('@') ? 'mailto:' + row.contacts : row.contacts">{{ row.contacts }}</a></p>
            </v-flex>
            <v-flex xs12 md2>
              <p class="hidden-md-and-up" style="font-family:MuseoBold; font-size:20px">Чей</p>
              <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px">{{ row.operator }}</p>
            </v-flex>
            <v-flex xs12 md2>
              <p class="hidden-md-and-up" style="font-family:MuseoBold; font-size:20px">От нас</p>
              <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px">{{ row.from_us }}</p>
            </v-flex>
            <v-flex xs12 md2>
              <p class="hidden-md-and-up" style="font-family:MuseoBold; font-size:20px">От них</p>
              <p style="overflow: hidden; text-overflow: ellipsis; max-width:300px">{{ row.from_them }}</p>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import YNPanel from '../components/YNPanel.vue'
  export default {
    components:{YNPanel},
    methods:{
      open_partner_dial(){
        this.temp_row = Object.assign({},{
          name: "",
          site: "",
          contacts: "",
          operator: "",
          from_us: "",
          from_them: ""
        })
        this.dialog = true;
      },
      open_edit_partner_dial(arg){
        this.edit_dialog = true;
        this.temp_row = Object.assign({},arg)
      },

      check_role(){
        return localStorage.role
      },
      add_partner(){
        if(this.$refs.new_form.validate())
          var data = {
            department: "Фандрайзинг",
            data: this.temp_row
          }
          axios.post('https://ocheredsut.ru/api/1/deps/', data).then((resp) =>{
            var data = resp.data.data
            data.id = resp.data.id
            this.rows.push(data)
            this.dialog = false
          })
      },
      delete_data(data){
        this.ynpanel = {
          header: data,
          visible: true,
          text: 'Удалить спонсора?'
        }
        this.ynpanel.function = (d => {
          axios.delete('https://ocheredsut.ru/api/1/deps/' + d.id).then((resp)=>{
            this.rows.splice(this.rows.indexOf(d), 1)
          })
        })

      },
      edit_partner(){
        if(this.$refs.edit_form.validate()){
            const data = {
              data: Object.assign({}, this.temp_row),
            }
            delete data.data.id
            axios.put('https://ocheredsut.ru/api/1/deps/'+this.temp_row.id, data).then((resp) =>{
              var data = resp.data.data
              data.id = resp.data.id
              var ind = this.rows.findIndex(a=>{return a.id === data.id})
              this.rows[ind] = data
              this.edit_dialog = false;
            })
        }
      },
      state_color(arg){
        const states = {
          'Согласился':'#1dd1a1',
          'Отказал':'#ee5253',
          'Написал':'#ff9ff3',
          'Не написал': '#c8d6e5'
        }
        return states[arg]
      }
    },
    created(){
      axios.get('https://ocheredsut.ru/api/1/deps/', {params:{department: "Фандрайзинг"}}).then((resp)=>{

        this.rows = resp.data.data.map(a=>{a.data.id = a.id; return a.data})
        this.operators = resp.data.dep_members.map(a=>{return a.info.name})
      })
    },
    data(){
      return {
        rules: {
          required: value => !!value.replace(/\s+/,'')  || 'Обязательное поле',
          min: v => v.length >= 8 || 'Минимум 8 букв'
        },
        edit_dialog: false,
        states:[
          {color:"#ff9ff3",name:"Согласился"},
          {color:"#ee5253",name:"Отказал"},
          {color:"#1dd1a1",name:"Написал"},
          {color:"#c8d6e5",name:"Не написал"}
        ],
        operators:[
          "Макеева",
          "И КО"
        ],
        ynpanel: {
          header: "",
          visible: false,
          text: ""
        },
        temp_row: {
          name: "",
          site: "",
          contacts: "",
          operator: "",
          from_us: "",
          from_them: ""
        },
        dialog: false,
        columns:[
          "Название",
          "Сайт",
          "Контакты",
          "Кто общается",
          "От нас",
          "От них"
        ],
        rows:[]
      }
    }
  }


</script>

<style>
</style>
