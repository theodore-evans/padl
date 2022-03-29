Search.setIndex({docnames:["README","advanced","advanced/saving","apidocs/padl","apidocs/padl.dumptools","apidocs/padl.dumptools.ast_utils","apidocs/padl.dumptools.inspector","apidocs/padl.dumptools.packagefinder","apidocs/padl.dumptools.serialize","apidocs/padl.dumptools.sourceget","apidocs/padl.dumptools.symfinder","apidocs/padl.dumptools.var2mod","apidocs/padl.exceptions","apidocs/padl.print_utils","apidocs/padl.transforms","apidocs/padl.util_transforms","apidocs/padl.utils","apidocs/padl.version","apidocs/padl.wrap","index","modules","usage","usage/apply","usage/combining_transforms","usage/creating_transforms","usage/debugging_your_transforms","usage/extras","usage/print_slice","usage/pytorch","usage/saving","usage/stages","usage/transform"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["README.md","advanced.md","advanced/saving.md","apidocs/padl.md","apidocs/padl.dumptools.md","apidocs/padl.dumptools.ast_utils.md","apidocs/padl.dumptools.inspector.md","apidocs/padl.dumptools.packagefinder.md","apidocs/padl.dumptools.serialize.md","apidocs/padl.dumptools.sourceget.md","apidocs/padl.dumptools.symfinder.md","apidocs/padl.dumptools.var2mod.md","apidocs/padl.exceptions.md","apidocs/padl.print_utils.md","apidocs/padl.transforms.md","apidocs/padl.util_transforms.md","apidocs/padl.utils.md","apidocs/padl.version.md","apidocs/padl.wrap.md","index.md","modules.md","usage.md","usage/apply.md","usage/combining_transforms.md","usage/creating_transforms.md","usage/debugging_your_transforms.md","usage/extras.md","usage/print_slice.md","usage/pytorch.md","usage/saving.md","usage/stages.md","usage/transform.md"],objects:{"":[[3,0,0,"-","padl"]],"padl.dumptools":[[5,0,0,"-","ast_utils"],[6,0,0,"-","inspector"],[7,0,0,"-","packagefinder"],[8,0,0,"-","serialize"],[9,0,0,"-","sourceget"],[10,0,0,"-","symfinder"],[11,0,0,"-","var2mod"]],"padl.dumptools.ast_utils":[[5,1,1,"","Position"],[5,2,1,"","get_position"],[5,2,1,"","get_source_segment"]],"padl.dumptools.inspector":[[6,1,1,"","CallInfo"],[6,2,1,"","caller_frame"],[6,2,1,"","caller_module"],[6,2,1,"","get_segment_from_frame"],[6,2,1,"","get_statement_at_line"],[6,2,1,"","instructions_are_the_same"],[6,2,1,"","non_init_caller_frameinfo"],[6,2,1,"","outer_caller_frameinfo"],[6,2,1,"","trace_this"]],"padl.dumptools.inspector.CallInfo":[[6,3,1,"","module"]],"padl.dumptools.packagefinder":[[7,4,1,"","RequirementNotFound"],[7,2,1,"","dump_requirements"],[7,2,1,"","get_distribution_name"],[7,2,1,"","get_packages"]],"padl.dumptools.serialize":[[8,1,1,"","Serializer"],[8,2,1,"","json_serializer"],[8,2,1,"","load_json"],[8,2,1,"","param"],[8,2,1,"","save_json"],[8,2,1,"","value"]],"padl.dumptools.serialize.Serializer":[[8,5,1,"","save"],[8,5,1,"","save_all"],[8,3,1,"","varname"]],"padl.dumptools.sourceget":[[9,1,1,"","ReplaceString"],[9,1,1,"","ReplaceStrings"],[9,2,1,"","cut"],[9,2,1,"","get_module_source"],[9,2,1,"","get_source"],[9,2,1,"","original"],[9,2,1,"","put_into_cache"],[9,2,1,"","replace"]],"padl.dumptools.sourceget.ReplaceString":[[9,5,1,"","cut"]],"padl.dumptools.sourceget.ReplaceStrings":[[9,5,1,"","cut"]],"padl.dumptools.symfinder":[[10,4,1,"","NameNotFound"],[10,1,1,"","Scope"],[10,1,1,"","ScopedName"],[10,2,1,"","find"],[10,2,1,"","find_in_ipython"],[10,2,1,"","find_in_module"],[10,2,1,"","find_in_scope"],[10,2,1,"","find_in_source"],[10,2,1,"","replace_star_imports"],[10,2,1,"","split_call"]],"padl.dumptools.symfinder.Scope":[[10,5,1,"","empty"],[10,5,1,"","from_level"],[10,5,1,"","from_source"],[10,5,1,"","global_"],[10,5,1,"","is_global"],[10,3,1,"","module_name"],[10,5,1,"","toplevel"],[10,5,1,"","unscoped"],[10,5,1,"","up"]],"padl.dumptools.var2mod":[[11,1,1,"","CodeGraph"],[11,1,1,"","CodeNode"],[11,1,1,"","Finder"],[11,1,1,"","Vars"],[11,2,1,"","find_codenode"],[11,2,1,"","find_globals"],[11,2,1,"","increment_same_name_var"],[11,2,1,"","rename"]],"padl.dumptools.var2mod.CodeGraph":[[11,5,1,"","build"],[11,5,1,"","dumps"],[11,5,1,"","print"]],"padl.dumptools.var2mod.CodeNode":[[11,5,1,"","from_source"]],"padl.dumptools.var2mod.Finder":[[11,5,1,"","find"],[11,5,1,"","generic_visit"],[11,5,1,"","get_source_segments"]],"padl.dumptools.var2mod.Vars":[[11,6,1,"","globals"],[11,6,1,"","locals"]],"padl.exceptions":[[12,4,1,"","WrongDeviceError"]],"padl.print_utils":[[13,2,1,"","combine_multi_line_strings"],[13,2,1,"","create_arrow"],[13,2,1,"","create_reverse_arrow"],[13,2,1,"","format_argument"],[13,2,1,"","make_bold"],[13,2,1,"","make_green"],[13,2,1,"","visible_len"]],"padl.transforms":[[14,1,1,"","AtomicTransform"],[14,1,1,"","Batchify"],[14,1,1,"","BuiltinTransform"],[14,1,1,"","ClassTransform"],[14,1,1,"","Compose"],[14,1,1,"","FunctionTransform"],[14,1,1,"","Identity"],[14,1,1,"","Map"],[14,1,1,"","Parallel"],[14,1,1,"","Pipeline"],[14,1,1,"","Rollout"],[14,1,1,"","TorchModuleTransform"],[14,1,1,"","Transform"],[14,1,1,"","Unbatchify"],[14,2,1,"","fulldump"],[14,2,1,"","group"],[14,2,1,"","importdump"],[14,2,1,"","load"],[14,2,1,"","save"]],"padl.transforms.ClassTransform":[[14,3,1,"","source"]],"padl.transforms.FunctionTransform":[[14,3,1,"","source"]],"padl.transforms.Pipeline":[[14,5,1,"","grouped"],[14,5,1,"","pd_forward_device_check"],[14,5,1,"","pd_to"]],"padl.transforms.TorchModuleTransform":[[14,5,1,"","pd_post_load"],[14,5,1,"","pd_pre_save"]],"padl.transforms.Transform":[[14,5,1,"","eval_apply"],[14,5,1,"","infer_apply"],[14,5,1,"","pd_call_in_mode"],[14,3,1,"","pd_device"],[14,3,1,"","pd_forward"],[14,5,1,"","pd_forward_device_check"],[14,5,1,"","pd_get_loader"],[14,3,1,"","pd_layers"],[14,3,1,"","pd_name"],[14,5,1,"","pd_parameters"],[14,5,1,"","pd_post_load"],[14,3,1,"","pd_postprocess"],[14,5,1,"","pd_pre_save"],[14,3,1,"","pd_preprocess"],[14,5,1,"","pd_save"],[14,3,1,"","pd_stages"],[14,5,1,"","pd_to"],[14,5,1,"","pd_varname"],[14,5,1,"","pd_zip_save"],[14,5,1,"","train_apply"]],"padl.util_transforms":[[15,1,1,"","IfEval"],[15,1,1,"","IfInMode"],[15,1,1,"","IfInfer"],[15,1,1,"","IfTrain"],[15,1,1,"","Try"]],"padl.utils":[[16,6,1,"","same"]],"padl.wrap":[[18,1,1,"","PatchedModule"],[18,2,1,"","transform"]],padl:[[3,1,1,"","Batchify"],[3,1,1,"","Identity"],[3,1,1,"","IfEval"],[3,1,1,"","IfInMode"],[3,1,1,"","IfInfer"],[3,1,1,"","IfTrain"],[3,1,1,"","Unbatchify"],[4,0,0,"-","dumptools"],[12,0,0,"-","exceptions"],[3,2,1,"","fulldump"],[3,2,1,"","group"],[3,2,1,"","importdump"],[3,2,1,"","load"],[3,2,1,"","param"],[13,0,0,"-","print_utils"],[3,2,1,"","save"],[3,2,1,"","transform"],[14,0,0,"-","transforms"],[3,7,1,"","unbatch"],[15,0,0,"-","util_transforms"],[16,0,0,"-","utils"],[3,2,1,"","value"],[17,0,0,"-","version"],[18,0,0,"-","wrap"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","function","Python function"],"3":["py","property","Python property"],"4":["py","exception","Python exception"],"5":["py","method","Python method"],"6":["py","attribute","Python attribute"],"7":["py","data","Python data"]},objtypes:{"0":"py:module","1":"py:class","2":"py:function","3":"py:property","4":"py:exception","5":"py:method","6":"py:attribute","7":"py:data"},terms:{"0":[0,3,6,9,10,11,14,25,26,27],"0x":11,"1":[0,2,3,6,7,9,10,11,14,15,23,25,26,27,28],"10":[0,3,15,24,25],"100":[2,11,23,24,26,27],"1000":[2,24],"1001":2,"11":[3,6,15],"123":6,"13":9,"2":[0,3,7,9,10,11,14,23,25,26,27],"20":0,"200":26,"244":23,"3":[0,3,5,6,7,10,11,14,23,25,26],"300":26,"4":[7,11,25,26],"5":[9,25],"6":25,"7":[0,25],"8":[0,5,25],"9":[0,9,25],"99":[3,15],"abstract":[0,14,19,25,31],"case":[2,3,9,10,14,23],"catch":[15,21],"class":[2,3,5,6,8,9,10,11,14,15,18,24,25,30],"const":2,"default":[2,3,6,8,10,14,15,23],"do":[0,2,3,12,14,21,22,24],"final":[15,26],"function":[0,2,3,6,8,10,11,14,18,19,23,24,25,31],"import":[0,2,3,7,10,11,14,15,18,19,22,23,24,25,26,29,30],"int":[5,6,9,10,11,13,14],"new":[9,10],"return":[0,2,3,6,7,8,9,10,11,14,22,23,24,26,27,30],"switch":[2,3,14,25],"throw":7,"true":[3,7,8,9,10,11,13,14,18,23,25,27],"try":[3,6,9,14,15,18,21,26],"var":11,A:[3,6,9,10,11,14,31],As:[2,11,30],At:25,By:[2,23],For:[2,7,10,23,24,25,26],If:[0,2,3,6,7,8,9,10,11,13,14,15],In:[3,9,10,14,23,24],It:[2,6,10,14,22,24,28],No:15,On:25,One:[2,14,23],The:[2,3,6,7,8,9,10,11,13,14,15,21,22,23,25,30,31],Then:25,These:[2,14],To:[2,3,9,14,22,23,30],With:31,_:2,__call__:[2,24],__file__:2,__init__:[2,6,24],__main__:[6,10],_ast:[10,11],_generatorwithlength:22,_pd_main:2,_thingfind:10,_trace_thi:6,a_transform:2,about:[0,6,14,25,28,31],abov:23,absolut:[2,25],accept:14,access:[10,27,30],account:6,ad:[3,10,14,22,31],adam:28,adapt:28,add:[2,3,9,14,24,26,27],add_n:2,addconst:2,addfirst:26,addit:9,addition:6,advanc:19,after:[2,3,14,25,28],again:2,ai:[0,19],airplan:22,alia:11,all:[0,2,6,8,11,12,14,18,19,21,22,23,28,29],allow:[0,9,10,19,22,23,26],along:28,also:[2,3,8,10,14,22,24,26],alwai:14,am:25,an:[0,2,6,7,9,10,11,13,14,19,22,25,26,28,31],analog:26,analysi:0,ani:[3,8,13,14,15],anoth:13,anyth:[2,6,19],apach:0,api:19,append:[2,8],appli:[2,3,13,14,15,19,21,23,25,30],applic:26,ar:[2,3,6,8,10,11,14,21,22,23,24,25,28,29,30],arbitrari:[0,19,26],arg:[2,6,14,22,25,27],argument:[2,3,6,10,13,14,22],argval:6,aris:23,arrai:[2,11,26],arrow:13,ascii:13,assign:[10,14],ast:[5,7,10,11],ast_nod:11,ast_util:[19,20],atom:14,atomictransform:[14,25],attribut:[6,9,14,16,25],augment:[23,26,28,30],automat:[2,3,14,22],avail:[6,22],awar:2,axxxxxxxxxxxxxxxxxxxx:9,b:[3,9,11,14,15],back:15,backward:28,bar:[11,22,23],base:[0,8,14,19],basic:[0,6],batch:[0,3,14,21,22,23,25,28,30,31],batch_siz:[22,25,28],batchifi:[3,10,14,21,25],baz:23,becaus:0,becom:[6,10,23,24],been:14,befor:[2,3,6,8,14,22],begin:6,behaviour:14,being:[3,14,26],below:[11,25],berlin:[0,19],between:[6,11,23],bia:25,big:2,bla:7,blip:7,blob:0,blog:19,blop:7,blu:7,bodi:[2,6,7,10,11],boilerpl:31,bold:13,bool:[3,6,9,10,11,14],both:[2,9,28],build:[0,2,10,11,19,31],build_my_transform:2,builder:[0,19],built:28,builtin:[11,14],builtintransform:14,bup:7,c:[3,14],cach:9,call:[3,6,8,10,11,14,15,24,25,30],call_info:14,call_sourc:10,callabl:[3,6,8,14,18,24],caller:6,caller_fram:6,caller_modul:6,callinfo:[6,14],calling_scop:10,can:[0,2,3,6,8,9,10,14,15,19,22,23,24,25,26,27,28,29,30,31],canb:22,cannot:[2,3,14],capabl:28,captur:16,carri:15,cat:22,catch_transform:15,caus:2,caveat:2,cell:9,central:31,chang:[2,6,15],charact:13,check:[6,14,25],checker:6,checkpoint:29,child:[12,14],child_transform:12,children:14,classifi:[23,30],classmethod:[8,10,11],classtransform:14,claus:15,clean:2,clip:0,close:26,co:25,code:[0,2,3,6,7,8,9,10,11,14,25,28,31],code_of_conduct:0,codegraph:[8,11],codenod:11,col:[9,11],col_offset:[5,11],collect:[9,14,21],column:6,com:0,combin:[13,14,19,21,24,31],combine_multi_line_str:13,come:[14,18,24],command:25,comment:6,common:23,complet:15,complex:[2,14,27,31],compon:[0,19,23],compos:[14,25,27,30],composit:23,comprehens:0,compress:[3,14],concat_low:26,concis:[0,21],condit:[15,21],condition:23,conduct:0,conflict:2,consid:2,consist:2,consol:25,constant:[2,9],construct:14,contain:[2,6,7,8,9,10,12,13,14,28,29],content:11,context:[6,14],continu:[23,30],contrast:14,contribut:19,control:14,conveni:28,convert:[0,10,11,19,24,28,30],coor:13,coordin:13,correct:14,correspond:[5,10,11,30],could:[2,10,23],count:[6,10],counter:[10,11],cpu:[3,14],creat:[0,2,6,7,8,10,11,13,14,19,21,22,23,28,29,31],create_arrow:13,create_reverse_arrow:13,crop:23,cuda:[14,28],current:[0,2,10,25],custom:[14,25,31],cut:9,d:25,data:[2,14,19,21,30,31],dataload:[14,22,31],datapoint:[14,23],dataset:2,dateutil:7,dc:0,debug:[11,19,21,31],debugg:25,decor:[3,14,18,24],deep:[0,2,19,23,30,31],deeper:25,def:[0,2,6,10,11,14,24,26,27,30],def_sourc:10,defin:[8,10,11,21,25,29,30],definit:2,depend:[2,11],descript:[2,3,8],detail:[6,14,23],determin:[3,6,9,10,11,14,18],dev:19,devblog:0,develop:[0,19],devic:[3,12,14,22],di:31,diagnos:25,dict:[9,14],dictionari:[2,14],differ:[2,3,8,9,22,25,30],diffus:0,dim:[3,14,25],dimens:[3,14,22,31],directli:14,directori:2,disabl:[3,13,14,22],disassebl:6,discard:0,displai:25,distribut:7,document:[6,14],doe:[14,22,25],doesn:[3,15],dog:22,don:[2,3,6,13,14,18],done:[14,22],down:[2,25],drop:[6,10],drop_n:[6,10],dump:[2,3,7,8,11,14],dump_requir:7,dumptool:[14,19,20],dure:[3,14,23,26],e:[3,10,14],each:[2,6,14,22,25,30],easili:31,ecosystem:[0,19],edg:11,edit:0,effect:2,either:[2,9],eleg:31,element:[14,23,25,30],elp:25,els:[3,6,11,15],else_:[3,15],else_transform:15,emb:25,embed:25,embedding_dim:25,empti:10,enabl:[2,3,14,31],end:[3,11,13,14],end_col_offset:[5,11],end_lineno:[5,11],enter:[6,25],entir:[24,25],entiti:10,entri:2,enumer:2,environ:0,epeat:25,equival:26,error:[15,25],escap:13,eval:[3,14,15,21,22,26],eval_appli:[3,14,15,22,25,26],evalu:30,even:23,event:6,everi:13,everyth:[11,21,23,24],exactli:23,exampl:[0,2,3,6,7,9,10,11,13,14,15,18,22,26,30],examplemodul:10,except:[7,10,15,19,20,21,25],execut:[0,2,6,23,25],exist:[3,11,14],expect:[2,3,9,14,22,25],explicit:[9,11],explicitli:14,extens:[3,14],extra:[15,19,21,28],f1:14,f2:14,f:[2,6,9,10,11,14],face:0,factori:16,fail:[2,3,6,14,15,25],fall:15,fals:[2,3,6,7,10,11,13,14,18],few:2,field:11,file:[2,3,9,14,26,29],file_suffix:8,fileexistserror:[3,14],filenam:[2,9,14,26],filter:11,filter_builtin:11,finally_transform:15,find:[0,7,10,11],find_codenod:11,find_glob:11,find_in_ipython:10,find_in_modul:10,find_in_scop:10,find_in_sourc:10,finder:11,fine:14,finish_right:13,first:[3,6,9,13,14,23],flat:23,flatten:[3,14,23],flexibl:31,folder:[2,3,14,29],follow:[2,6,10,11,21,25],foo:[7,11,14,23],forc:2,force_overwrit:[3,14],form:[10,24,31],formal:31,format:[7,13,30,31],format_argu:13,forward:[0,14,19,21,22,24,25],found:[2,3,6,7,10,11,14],four:10,frame:[6,9],frameinfo:6,from:[0,3,6,7,9,10,11,14,15,19,22,24,25,26,28,29,30],from_:11,from_col:9,from_level:10,from_lin:9,from_sourc:[10,11],full:[0,2,3,14],full_dump_module_nam:11,fulldump:[2,3,14],fulli:[3,14],functiontransform:14,fundament:14,futur:2,g:[10,14],gan:0,gener:[0,14,22],generic_visit:11,germani:[0,19],get:[2,5,6,7,9,10,11,13,14,16,19,21,23,25,26],get_distribution_nam:7,get_module_sourc:9,get_packag:7,get_posit:5,get_segment_from_fram:6,get_sourc:9,get_source_seg:[5,11],get_statement_at_lin:6,getitem:[6,27],github:0,give:9,given:[3,6,7,9,10,11,14],global:[2,10,11],global_:10,globals_:11,go:[0,11,25],good:14,got:25,gotten:9,gpu:[14,22,30,31],gradient:[14,22,31],grain:14,graph:11,great:[0,19],green:13,group:[3,14,21],guid:0,h:25,ha:[2,9,10,11,14,23,25,28,30],hacki:6,handl:22,happen:[15,30],have:[0,2,10,14,19,28],head:23,hello:26,help:[14,25],helper:[3,8],here:[2,6,10,25],hidden:24,hierarchi:10,histori:10,hood:22,how:[10,14,22,23,24,27,29,30,31],http:0,i:[2,3,10,14,25],id:9,ident:[3,14,15,21,27],identifi:10,if_:[3,15],ifev:[3,15,21,26],iff:10,ifinf:[3,15,21,26],ifinmod:[3,15],iftrain:[3,15,21,23,26],ignor:[2,14],ignore_grad:14,ignore_scop:[3,6,14,18],iim:[3,15],imag:[0,13,30],implement:[14,24],importdump:[2,3,14],in_featur:25,includ:[2,6,9,14,28,29],incorpor:25,increment:11,increment_same_name_var:11,index:14,indic:[7,10,14],individu:23,infer:[3,14,15,21,22,26,28,30],infer_appli:[3,14,15,22,25,26],infer_pipelin:28,inform:[6,14,25],initi:[2,14,28],inlin:[6,14],innov:[0,19],input:[3,9,13,14,22,23,25,26],insert:9,insid:[15,25],inspect:[0,6,9,14,25,31],inspector:[14,19,20],instal:2,instanc:[2,22,23,24,28],instead:[2,3,6,14,18],instr:6,instruct:6,instructions_are_the_sam:6,interact:[0,2,25,29,31],interest:0,intern:22,interpret:0,introduct:19,invers:[3,14],involv:6,io:0,ipython:[0,2,9,10,27],is_glob:10,isinst:[9,11,18],issu:0,item:[0,3,10,14,16,22,26],iter:[14,22,28],its:[10,11,14,25],jpg:22,json:[2,8],json_seri:8,jupyt:0,just:[2,3,14],keep:23,kei:9,keyword:[0,2,3,14,19],know:21,kwarg:[3,6,14],l1:24,l2:24,lab:[0,19],lambda:[3,14,15,23,24,25,26],larg:2,last:[2,9,13,14],layer1:28,layer2:28,layer:[0,14,19,25],learn:[0,19,22,23,24,28,29,30,31],len:[2,22],length:[13,23],let:25,level:[2,6,10,23,25],lf1:[0,19],licens:19,like:[2,7,22,30],limit:2,lin:24,line:[6,9,10,13,25],linear:[0,24,25],lineno:[5,6,10,11],list:[2,3,6,7,9,10,11,13,14,15,22,25,26,28],liter:[3,6,14,15],live:11,load:[0,2,3,6,8,14,19,21,22,23,28,30],load_data:2,load_funct:8,load_imag:[23,30],load_json:8,loader:[8,14],loc:9,local:11,locat:[9,10],log10:24,longtensor:25,look:[0,2,6,10],lookup:[28,30],loop:[10,22,28],loss:[0,19,23,28],lower:26,lr:28,macro:23,made:[6,14],mai:[0,19],main:[0,10,12],mainli:6,maintain:9,make:[0,13,19,21,25,28],make_bold:13,make_green:13,manual:0,map:14,mark:[3,8,14],match:[3,6,12,14,15,25],math:24,md:0,mean:[2,3,14,23],messag:7,messi:2,method:[6,14,21,26],might:[2,26],minim:31,minus100:24,minusx:[24,26,27],mlp:24,mml:24,mnist:0,mode:[3,14,15,22],model:[0,2,14,19,28,30],model_pass:23,modifi:9,modul:[0,3,6,7,8,9,10,11,14,18,19,21,23,24,27,29,30],module_nam:[6,10],more:[0,2,3,6,14,23,31],most:[10,23,30],mother:12,mother_transform:12,move:[3,14,23,25],mpiler:25,msg:7,much:[2,31],multi:[13,31],multipl:[2,14,22,24,28],multiprocess:14,must:[2,6,14,23],my:2,my_classifi:[22,30],my_classifier_transform:[23,30],my_pipelin:[0,2,28,29],myfil:2,myfunct:6,mykei:9,myload:2,mypipelin:29,mypytorchlay:28,mysav:2,mytransform:2,n:[6,10,11,14],n_final_row:13,n_in:24,n_initial_row:13,n_out:24,n_to_add:2,name:[2,3,6,7,8,10,11,14,15,30],namenotfound:10,natur:22,need:[2,8,14,19],nest:[10,27,28],never:14,next:[22,23,24,27,28,29,30,31],nextmodul:6,nlp:0,nn:[0,14,24,25],node:[5,7,10,11],nodetyp:11,nodevisitor:11,non:9,non_init_caller_frameinfo:6,none:[3,6,8,10,11,14,15,18],normal:[2,9,14],not_found:2,note:[2,6],notebook:[2,31],noth:[3,14,21],now:2,np:[2,11,18,24,26],nput:25,npy:2,nth:23,num_embed:25,num_work:[22,25,28],number:[6,10,11,13],numpi:[2,18,24],o:11,object:[6,9,10,11,14,22,26],occur:15,offset:[6,11],often:26,one:[2,3,10,13,14,15,23,25,30],onli:[2,11,23,26],open:[2,23,26],open_fil:26,oper:[6,23],opnam:6,optim:28,option:[3,6,8,11,14,15],order:[2,14],ordereddict:14,origin:[6,9],other:[14,15],otherwis:[3,14,15],out:[9,10,11,15,18,23,24],out_featur:25,outer:6,outer_caller_frameinfo:6,output:[3,14,15,22,23,30],over:[13,14,23,28],overlap:9,overrid:[3,14],overridden:[2,3,8],overwrit:[3,14],own:[2,25],p:25,packag:[0,2,3,7,14,19,25],packagefind:[19,20],pad:13,padl:[2,20,23,24,25,26,27,29,30,31],padl_value_0:2,page:21,parallel:[3,14],param:[2,3,8,14],paramet:[3,6,7,8,9,10,11,12,13,14,15,18,29],parent:[2,18],parenthes:23,pars:[0,7,11],part:[9,14,21,22,25,30],parti:2,particular:24,pass:[0,2,3,14,19,22],patch:18,patchedmodul:18,path:[2,3,8,14,23,30],pathlib:[2,3,8,14],pd_call_in_mod:14,pd_debug:[21,25],pd_devic:14,pd_forward:[14,22,30],pd_forward_device_check:14,pd_get_load:14,pd_group:14,pd_layer:[14,28],pd_name:[14,15],pd_np:18,pd_paramet:[14,28],pd_post_load:14,pd_postprocess:[14,30],pd_pre_sav:14,pd_preprocess:[14,30],pd_save:14,pd_save_opt:14,pd_stage:14,pd_to:[14,28],pd_varnam:14,pd_zip_sav:14,perform:[3,14,15],pick:2,piec:[10,11],pil:23,piltotensor:23,pip:0,pipelin:[0,14,19,21,22,24,25,27,28,29,30],pleas:0,pluson:2,plustwo:2,posit:[5,9,11,25],possibl:[2,6,14,24,28],post:[0,14,19,30],postprocess:[3,14,19,21,22,23,25],potenti:2,power:23,pre:[0,9,14,19,30],preced:13,precis:29,predict:[23,28],prefer:0,prepar:0,preprocess:[3,14,19,21,22,23,25,28,31],preprocess_imag:23,pretti:27,prevent:[2,3,14],previous:2,print:[3,6,11,13,14,19,21,25,29],print_util:[19,20],process:[0,2,14,19,22,30,31],produc:25,progress:22,prompt:0,propag:14,properti:[6,8,10,14],provid:[2,23,25],pt:2,put:9,put_into_cach:9,py:[2,29],python:[0,2,5,6,7,10,11,19,23,24,29],pytorch:[0,14,19,21,22,23,24,27,29,30],q:25,quit:25,r:25,rais:[3,14,25],rand:18,random:18,randomresizedcrop:23,randomrot:23,rang:2,ransform:25,rather:[6,14],re:[0,19,23],reach:25,read:[0,2,21,22,26,27,31],read_from_path:26,readabl:30,recent:10,recommend:0,recreat:2,recurs:[3,14,25],ref:25,refer:21,regardless:15,relev:25,reli:0,relu:24,rememb:28,remov:[3,14,22],renam:[2,11],rename_loc:11,repeat:[2,23,25],repl:9,replac:[9,10],replace_cach:9,replace_star_import:10,replacestr:9,repres:[10,11],reproduc:31,requir:[2,3,6,7,14,29],requirementnotfound:7,reshap:30,resiz:23,resnet18:[23,30],respect:[3,11,14,26],respons:[2,30],rest:6,result:[2,3,9,14,23],retriev:25,return_loc:6,return_parti:10,revers:2,roll:23,rollout:[3,14],rstring:9,run:25,runtimeerror:25,s:[0,3,6,8,9,10,14,15,21,22,24,28,29,30],same:[3,5,6,9,10,11,14,16,21,23,25,28],save:[0,1,3,8,14,19,21,22,31],save_al:8,save_funct:8,save_json:8,saver:8,scope:[3,6,10,11,14,18],scoped_nam:[10,11],scopednam:[10,11],scopelist:10,search:[10,11,14],second:[2,3,10,14,23],section:[9,22,23,24,27,28,29,30,31],see:[0,2,3,6,8,14,22],segment:[5,6,10,11],segment_typ:6,self:[2,10,14,24],send:[14,22,28,31],sentiment:0,sequenc:[13,14,23],seri:14,serial:[3,14,19,20],session:[0,2,29],set:[2,8,11,14,22],settrac:6,shape:25,should:[2,3,6,8,14],show:[22,25],shown:25,simpl:0,simpli:[2,14],sin:24,sinc:25,singl:[0,14,19,22,23],size:[22,25],slice:[19,21,29,31],slower:0,so:[10,23,25],some:[2,6,23,25,28],somemodul:11,someobject:2,someth:[2,26],sometim:2,soon:[0,6],sourc:[0,5,6,7,9,10,11,14],sourceget:[19,20],space:13,special:[23,26,30],specifi:[2,3,8,9,10,14,22],split:[2,10],split_cal:10,stack:6,stage:[14,19,21,22,23,25],stand:30,standard:[0,19],star:[2,10],start:[3,10,13,14,19,21,25],start_left:13,state_dict:28,statement:[2,3,6,10,14,15,25],step:[23,28],stop:31,store:[2,3,8,28,29],str:[2,3,6,7,8,9,10,11,13,14,15],strict:7,strict_requir:[2,3,14],string:[3,6,7,8,9,10,11,13,14],sub:[9,11,14,23,27],subclass:10,subleti:6,substr:9,subval:2,successfulli:15,suffix:2,suggest:30,superimpos:13,support:[0,2,22],surround:10,sy:6,symbol:[2,10],symfind:[6,11,19,20],t1:[14,23,27],t2:[14,23,27],t3:[14,23,27],t4:27,t5:27,t:[2,3,6,7,13,14,15,18,23,25,26],take:[13,23],taken:[9,24],target:23,target_instr:6,target_mod:[3,15],tensor:[0,3,14,22],text:[0,2],textcorpu:2,than:2,them:[2,3,14,21,23,28],therefor:0,thereof:[3,14],thi:[0,2,3,6,9,10,11,13,14,15,22,23,24,25,27,28,29],thing:[2,3,8,9,10,11],third:2,those:[2,11,28,30],three:[22,23],through:[11,22,23],thu:[2,23],time:2,to_col:9,to_lin:9,to_tensor:25,toarrai:2,togeth:27,too:[24,27,29],top:[10,13,25],topic:19,topk:0,toplevel:[3,6,10,14,18],topolog:[0,19],torch:[0,14,24,25,28],torchmoduletransform:14,torchvis:[23,30],totensor:[23,30],tqdm:22,trace:6,trace_thi:6,tracefunc:6,track:2,train:[3,14,15,21,22,26,28,30],train_appli:[14,22,25,28],train_data:28,train_model:28,train_pipelin:28,training_pipelin:23,transform:[0,3,10,12,15,16,18,19,20,21,27,29,30],transform_or_modul:[3,14],transpar:[13,31],tree:[0,10,11],tupl:[2,3,6,10,11,14,15,23],turn:14,tvt:23,two:[2,6],txt:[2,7,29],type:[0,6,11],typic:14,u:25,uit:25,unbatch:[0,3,21,23,30],unbatchifi:[3,14],under:[0,22],undo:2,unfortun:0,union:[3,14,15],uniqu:14,unscop:10,unsqueez:[3,14],until:25,up:[2,10,25],updat:22,us:[0,2,3,6,7,8,9,10,11,13,14,15,18,19,21,22,23,24,25,26,27,30,31],usag:[0,19],use_default:[2,3,8],use_replace_cach:9,user:[0,2,19,25],usual:[2,30],util:[6,7,13,14,19,20,23,28],util_transform:[19,20],val:[2,3,8],valu:[3,6,8,9,10,13,21],var2mod:[19,20],var_nam:10,variabl:[10,11,14,25],variou:[9,10],varnam:[8,10],veri:2,version:[0,2,7,9,10,14,19,20],via:[2,14,27,28,29,30],view:23,visibl:13,visible_len:13,visitor:11,w:25,wa:[0,6,7,14,19,25],wai:[10,25],want:[2,26],warn:[0,3,14],wasn:7,we:[0,2,25,30],well:10,were:[2,10],what:[14,26,30],whatev:14,when:[0,2,3,8,14,15,24,25,28,29],where:[6,9,11,13,25],wherea:30,which:[2,3,6,9,10,11,14,22,23,29],whole:[14,31],whose:[3,14],wide:6,within:[9,10,14,28],without:[3,8,31],word:2,word_index:2,wordindex:2,work:[0,27,28,31],worker:22,workflow:[30,31],worri:31,would:[2,9,10,23],wrap:[2,3,14,19,20,24],wrap_typ:14,wrappe:[3,18],wrapper:[3,18,24],write:[0,2,3,14,19],written:10,wrongdeviceerror:12,x1:14,x2:14,x3:14,x:[0,2,3,7,9,10,11,13,14,15,23,24,25,26,27,30],xxxx:9,xxxxxaxxxxxxxxxxxxxxxxxxxx:9,xxxxxxxxxxx:9,xxxxxxxxxxxxxb:9,xxxxxxxxxxxxxbxxxx:9,y:[2,11,13,23,24,27],you:[0,2,19,23,26,31],your:[2,19,21,31],z:[11,23],zero_grad:28,zip:[3,14]},titles:["Introduction","Advanced Topics","Saving","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.ast_utils</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.inspector</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.packagefinder</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.serialize</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.sourceget</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.symfinder</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.dumptools.var2mod</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.exceptions</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.print_utils</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.transforms</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.util_transforms</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.utils</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.version</span></code>","<code class=\"docutils literal notranslate\"><span class=\"pre\">padl.wrap</span></code>","Welcome to PADL\u2019s documentation!","API Documentation","Usage","Applying Transforms to Data","Combining Transforms into Pipelines","Creating Transforms","Debugging your Transforms","Extras","Printing and Slicing","Using PyTorch Modules with Transforms","Saving and Loading","Stages: Preprocess, Forward and Postprocess","<em>Transforms</em> and <em>Pipelines</em>"],titleterms:{"import":21,"try":0,The:26,access:28,advanc:1,an:23,anyth:21,api:20,appli:[22,26],ast_util:5,automat:28,block:2,blog:0,build:23,colab:0,combin:23,compos:23,content:[1,19,20,21],contribut:0,convert:23,creat:24,custom:2,data:22,debug:25,defin:2,depend:26,dev:0,devic:28,dict:28,dictionari:23,differ:23,document:[19,20],doe:2,dumptool:[4,5,6,7,8,9,10,11],exampl:[23,25],except:[12,26],extra:26,extract:23,first:0,forward:[23,30],from:[2,21,23],gener:23,get:0,group:23,handl:26,how:2,imag:23,inspector:6,instal:0,introduct:0,item:23,layer:28,licens:0,load:29,loop:2,map:23,mode:26,model:23,modul:[2,28],multipl:23,mutat:2,need:21,nest:2,notebook:0,object:2,other:2,out:0,packagefind:7,padl:[0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,28],parallel:23,paramet:[2,28],pass:23,pipelin:[23,31],post:23,postprocess:30,pre:23,preprocess:30,print:27,print_util:13,process:23,program:0,pytorch:[2,28],resourc:0,rollout:23,s:19,same:26,sampl:23,save:[2,28,29],scope:2,serial:[2,8],share:28,slice:27,sourceget:9,stage:30,start:0,state:28,symfind:10,target:2,tensor:23,topic:1,train:23,transform:[2,14,22,23,24,25,26,28,31],us:28,usag:21,util:[16,26],util_transform:15,valu:2,var2mod:11,variabl:2,version:[17,23],weight:28,welcom:19,what:2,within:2,work:2,wrap:18,you:21,your:[0,25]}})