<template>
  <v-container fluid>
    <YNPanel :func="ynpanel.function" @no="ynpanel.visible = false" :visible="ynpanel.visible" :header="ynpanel.header" :text="ynpanel.text"></YNPanel>

    <Comments :key="TaskComment.title" :header="TaskComment.title" :comments="TaskComment.comments" :visible="TaskComment.visible" @close="TaskComment.visible = false" @add_comment="add_comment"></Comments>

    <v-dialog v-model="new_task_dialog" max-width="500px">
    <v-card class="rounded">
      <v-card-title class="headline">
        <p>Новая задача</p>
      </v-card-title>
      <v-card-text>
        <v-form ref="fillform">
          <v-layout align-center row wrap>

            <v-flex xs12>
              <v-text-field
                :rules="[rules.required]"
                v-model="temp_block.title"
                label="Заголовок"
                prepend-icon="list_alt"
                color="orange"
              ></v-text-field>
            </v-flex>

            <v-flex xs12>
              <v-textarea
                :rules="[rules.required]"
                v-model="temp_block.description"
                prepend-icon="mode_comment"
                label="Описание"
                color="orange"
              ></v-textarea>
            </v-flex>

            <v-flex xs12>
              <v-menu
                :close-on-content-click="false"
                v-model="date_menu"
                transition="scale-transition"
                offset-y
                :nudge-right="40"
                prepend-icon="mode_comment"
                max-width="290px"
                min-width="290px"
                color="orange"
              >
                <v-text-field
                  slot="activator"
                  label="Дедлайн"
                  :value="formattedDate(temp_block.deadline)"
                  prepend-icon="event"
                  readonly
                  color="orange"
                ></v-text-field>
                <v-date-picker color="orange" v-model="temp_block.deadline" no-title>
                    <v-btn flat color="orange" @click="date_menu = false"><p>Сохранить</p></v-btn>
                </v-date-picker>
              </v-menu>
            </v-flex>
            <v-flex xs12>
              <v-autocomplete
                v-model="temp_block.responsibles"
                :items="responsibles"
                chips
                color="orange"
                label="Ответственные"
                item-text="name"
                return-object
                prepend-icon="people"
                multiple
              >
                <template
                  slot="selection"
                  slot-scope="data"
                >
                  <v-chip
                    :selected="data.selected"
                    close
                    class="chip--select-multi"
                    @input="data.parent.selectItem(data.item)"
                  >
                    <v-avatar>
                      <img :src="data.item.pic">
                    </v-avatar>
                    {{ data.item.name.split(' ')[1] }}
                  </v-chip>
                </template>
                <template
                  slot="item"
                  slot-scope="data"
                >
                  <template>
                    <v-list-tile-avatar>
                      <img :src="data.item.pic">
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                      <v-list-tile-title v-html="data.item.name.split(' ')[1]"></v-list-tile-title>
                      <v-list-tile-sub-title v-html="data.item.faculty"></v-list-tile-sub-title>
                    </v-list-tile-content>
                  </template>
                </template>
              </v-autocomplete>
            </v-flex>
          </v-layout>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-layout justify-end row wrap>

          <v-flex text-xs-right sm3 xs6>
            <v-btn flat color="red" @click="new_task_dialog=false"><p>Закрыть</p></v-btn>
          </v-flex>

          <v-flex text-xs-right sm3 xs6>
            <v-btn flat color="green" @click="temp_block.function()"><p>Добавить</p></v-btn>
          </v-flex>

        </v-layout>
      </v-card-actions>
    </v-card>
    </v-dialog>

    <v-layout class="hidden-sm-and-up" row wrap>
      <v-flex xs4 text-xs-center v-for='type in types' :key="type.name">
        <v-btn flat block @click="filter = type.name" :color="type.color"><p>{{type.rusname}}</p></v-btn>
      </v-flex>
    </v-layout>

    <v-layout row wrap>
      <v-flex xs12 md4 v-for="type in filter_types" :key="type.name" px px-1>
        <div class="headline text-xs-center"><p>{{type.rusname}}</p></div>
        <v-card flat :style="'border-top:solid; border-width: 5px; background-color:#f1f2f6; border-color:' + type.color">
          <v-layout row wrap>
            <v-flex pa-2 xs12 :key="task.id" v-for="task in columns.filter(a => {return a.type === type.name}).sort((a, b)=>{return a.deadline > b.deadline ? 1: -1})">
              <v-card class="rounded">

                <div style="display: flex; float:right; flex-direction: column">
                  <v-btn small v-if="check_role() > 724" @click="task_delete(task)" flat icon><v-icon small color="red">close</v-icon></v-btn>
                  <v-btn small v-if="check_role() > 204" @click="change_dialog(task)" flat icon><v-icon small color="primary">edit</v-icon></v-btn>
                  <div v-if="check_role() > 204">
                    <v-menu offset-y>
                        <v-btn small slot="activator" icon><v-icon>menu</v-icon></v-btn>
                      <v-list>
                        <v-list-tile
                          v-for="(item, index) in types"
                          :key="index"
                          @click="changetype(task, item.name)"
                        >
                          <v-list-tile-title :color="type.color">{{ item.rusname }}</v-list-tile-title>
                        </v-list-tile>
                      </v-list>
                    </v-menu>
                  </div>
                </div>




                  <div class="pa-3">
                    <div class="grey--text text--darken-3 title"><p style="width: 90%">{{task.title}}</p></div>
                    <div class="pt-4 grey--text text--darken-2" pt-2><p>{{task.description}}</p></div>
                  </div>
                  <v-layout style="width:100%" class="pa-2" align-center row wrap>
                  <v-flex xs12 md4>
                    <v-layout row wrap>

                      <v-flex xs2 pl-1 v-for="user in task.responsibles.slice(0, 3)" :key="user.id">
                        <v-tooltip top>
                          <v-avatar
                            size="35px"
                            slot="activator"
                          >
                            <v-img :src="user.pic" alt="alt"></v-img>
                          </v-avatar>
                          <span><p>{{user.name}}</p></span>
                        </v-tooltip>
                      </v-flex>

                      <v-flex xs1 pl-2 v-if="task.responsibles.length > 3" class="headline">...</v-flex>

                    </v-layout>
                  </v-flex>
                  <v-flex xs12>
                    <v-layout justify-space-between align-center row>
                      <div>
                        <v-btn @click="open_comment(task)" icon><v-icon color="pink lighten-2">chat</v-icon><p>{{ task.comments.length}}</p></v-btn>
                      </div>

                      <div text-xs-left class="grey--text text--darken-2"><p><v-icon>date_range</v-icon>До: {{ task.deadline ? formattedDate(task.deadline) : 'Отсутствует'}}</p></div>


                    </v-layout>
                  </v-flex>
                  <div class="pa-2">
                    <div class="caption"><p>Создано: {{task.author.name.split(" ")[0]}} {{task.author.name.split(" ")[1]}}</p></div>
                    <div class="caption"><p>Дата создания: {{formattedDate(task.author.created * 1000)}}</p></div>
                  </div>

                </v-layout>

              </v-card>
            </v-flex>
            <v-flex v-if="type.name != 'done'" xs12>
              <v-btn flat color="green" @click="add_dialog(type)" prepend-icon><v-icon>add</v-icon> Добавить</v-btn>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import format from 'date-fns/format'
import Comments from '../components/Comments.vue'
import YNPanel from '../components/YNPanel.vue'
import axios from 'axios'

  export default {
    props: ['department'],
    components: {Comments, YNPanel},
    computed: {
      nowtime(){
        return new Date()
      },
      filter_types(){
        if(this.filter){
          return [this.types[this.filter]]
        }
        else{
          return this.types
        }
      },
      dep(){
        return this.$route.params.dep
      }
    },
    methods:{
      add_dialog(type){
        this.temp_block = {
          title: "",
          deadline: "",
          description: "",
          responsibles: [],
          comments: [],
          type: type.name,
          function: this.add_task
        }
        this.new_task_dialog = true
      },
      change_dialog(task){
        this.temp_block = task
        this.temp_block.function = this.change_task
        this.new_task_dialog = true
      },
      change_task(){
        if(this.$refs.fillform.validate()){
          var task = Object.assign({}, this.temp_block)
          delete task.function
          task.department = this.get_path_name(this.$route.params.dep)
          axios.put('https://ocheredsut.ru/api/1/task/' + task.id, task).then((resp) => {
            this.temp_block = {
              title: "",
              deadline: "",
              description: "",
              responsibles: [],
              comments: [],
              type: ""
            }
            this.new_task_dialog = false;
          })

        }
      },
      check_role(){
        return localStorage.role
      },
      get_path_name(path){
        var dictionary = [
          {
            name: "Все",
            path: "All",
          },
          {
            name: "Фильтрация",
            path: "Filtration",
          },
          {
            name: "Серфинг",
            path: "Surfing",
          },
          {
            name: "Event",
            path: "Event",
          },
          {
            name: "Приемная комиссия",
            path: "PK",
          },
          {
            name: "Собеседники",
            path: "Companions",
          },
          {
            name: "Фандрайзинг",
            path: "Fundraising",
          },
          {
            name: "SMM",
            path: "SMM",
          },
        ]
        return dictionary.find(a=>{return a.path === path}).name
      },
      formattedDate(arg){
        return arg? format(arg, 'D.MM.YYYY') : ''
      },
      changetype(column, type){
        const data = {
            type: type
        }
        axios.put('https://ocheredsut.ru/api/1/task/' + column.id, data).then((resp) => {
          column.type = type
        })
      },
      task_delete(task){
        task.name = task.title
        this.ynpanel = {
          header: task,
          visible: true,
          text: 'Удалить?'
        }
        this.ynpanel.function = (arg => {
          axios.delete('https://ocheredsut.ru/api/1/task/' + arg.id).then((resp) => {
            this.columns.splice(this.columns.indexOf(arg), 1)
            this.delete_dialog = false;
          })

        })
      },
      add_task(){
        if(this.$refs.fillform.validate()){
          var task = Object.assign({}, this.temp_block)
          delete task.function
          task.department = this.get_path_name(this.$route.params.dep)
          axios.post('https://ocheredsut.ru/api/1/kanban/' + this.get_path_name(this.$route.params.dep), task).then((resp) => {
            this.columns.push(resp.data)
            this.temp_block = {
              title: "",
              deadline: "",
              description: "",
              responsibles: [],
              comments: [],
              type: ""
            }
            this.new_task_dialog = false;
          })

        }
      },
      add_comment(arg){
        const data = {
          comment: arg
        }
        axios.post('https://ocheredsut.ru/api/1/task/'+this.TaskComment.id, data).then((resp)=> {
          this.TaskComment.comments = resp.data.comments
        })
      },
      open_comment(arg){
        this.TaskComment.id = arg.id
        this.TaskComment.comments = arg.comments
        this.TaskComment.title = arg.title
        this.TaskComment.visible = true
      },
    },
    mounted(){
      axios.get('https://ocheredsut.ru/api/1/kanban/' + this.get_path_name(this.department)).then((resp) => {
        this.columns = resp.data.tasks
        this.responsibles = resp.data.responsibles.map(a=>{return a.info})
      })
    },
    data(){
      return{
        ynpanel: {
          visible: false,
          header: '',
          text: ''
        },
        rules: {
          required: value => !!value.replace(/\s+/, "")  || 'Обязательное поле',
          min: v => v.length >= 8 || 'Минимум 8 букв'
        },
        filter: "",
        TaskComment: {
          title: '',
          comments: {},
          visible: false
        },
        types:{
          todo: {
            name: "todo",
            rusname: "Идеи",
            color: "#3498db"
          },
          doing: {
            name: "doing",
            rusname: "В работе",
            color: "#f1c40f"
          },
          done: {
            name: "done",
            rusname: "Сделано",
            color: "#2ecc71"
          }
        },
        columns:[],
        temp_block:{
          title: "",
          deadline: "",
          description: "",
          responsibles: [],
          comments: [],
          type: ""
        },
        new_task_dialog: false,
        date_menu: false,
        responsibles: [
          {
            name: "Влад Ковальчук",
            pic: "https://pp.userapi.com/c853516/v853516777/7f0f4/N3VYmXqbdgk.jpg",
            faculty: "ИСиТ"
          }
        ]
      }
    }
  }
</script>

<style>
</style>
