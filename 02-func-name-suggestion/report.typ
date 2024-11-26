#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 1.5cm),
)

#set text(
  size: 14pt
)

#let caption(body) = text(fill: clr-caption)[
  #par[
    #body
  ]
]

#align(center)[
  #text(18pt)[*AI4SE. Лабораторная №2. Генерация имени функции по ее телу*]

  #text(16pt)[Гранат Артемий Максимович, МСП241]
]

= Описание решения

Для генерации имен функции были использованы языки Python и Ruby. При обработке
данных с помощью запросов Tree-sitter были извлечены имя и тело функции, при
этом были выделены комментарии для их удаления в дальнейшем. После этого при
проходе по AST были удалены комментарии, тело без комментариев помещено в
отдельный столбец датасета.

Для генерации имён была использована модель `Salesforce/codet5p-220m`. Для
работы с данной моделью к телу функции перед генерации был приставлен префикс
`def <extra_id_0> :`, что подходит как для Python, так и для Ruby. В связи с
нехваткой вычислительных ресурсов модель обработала только первые 500 функций
из датасета.

= Воспроизведение

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt -r requirements_dev.txt
./benchmark.sh
```

= Метрики

== Python (тело без комментариев)

#table(
  columns: 2,
  [Метрика], [Значение],
  [Количество точных предсказаний], [110],
  [ExactMatch], [0.14],
  [Rouge1], [0.35195695970696],
  [Rouge2], [0.1695556277056277],
  [RougeL], [0.35087442002442026],
  [RougeLSum], [0.3496014041514043],
)

== Python (тело с комментариями)

#table(
  columns: 2,
  [Метрика], [Значение],
  [Количество точных предсказаний], [155],
  [ExactMatch], [0.212],
  [Rouge1], [0.5004349206349212],
  [Rouge2], [0.26611428571428575],
  [RougeL], [0.49755634920634983],
  [RougeLSum], [0.4989579365079372],
)

== Ruby (тело без комментариев)

#table(
  columns: 2,
  [Метрика], [Значение],
  [Количество точных предсказаний], [161],
  [ExactMatch], [0.196],
  [Rouge1], [0.3811611111111113],
  [Rouge2], [0.14191666666666664],
  [RougeL], [0.3803388888888892],
  [RougeLSum], [0.381000793650794],
)
== Ruby (тело с комментариями)
#table(
  columns: 2,
  [Метрика], [Значение],
  [Количество точных предсказаний], [162],
  [ExactMatch], [0.204],
  [Rouge1], [0.38968571428571463],
  [Rouge2], [0.14673333333333333],
  [RougeL], [0.3896388888888891],
  [RougeLSum], [0.3900357142857146],
)

= Слабые места

Среди плохо сгенерированных имён функций можно выделить следующее (повторяется
на обоих языках):

1. Пустые строки
2. Строки, состоящие из символов (`&&`, `_`, `=`, `-`)
3. Строки, состоящие из одного слова (`run`: `run_what?`, `md5`, ...)

== Примеры

1.
```
Prediction: ' '
Functions:
def dictify(r,root=True):
    """http://stackoverflow.com/a/30923963/2946714"""
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d

def get_mgtv_real_url(url):
        """str->list of str
        Give you the real URLs."""
        content = loads(get_content(url))
        m3u_url = content['info']
        split = urlsplit(m3u_url)
        
        base_url = "{scheme}://{netloc}{path}/".format(scheme = split[0],
                                                      netloc = split[1],
                                                      path = dirname(split[2]))

        content = get_content(content['info'])  #get the REAL M3U url, maybe to be changed later?
        segment_list = []
        segments_size = 0
        for i in content.split():
            if not i.startswith('#'):  #not the best way, better we use the m3u8 package
                segment_list.append(base_url + i)
            # use ext-info for fast size calculate
            elif i.startswith('#EXT-MGTV-File-SIZE:'):
                segments_size += int(i[i.rfind(':')+1:])

        return m3u_url, segments_size, segment_list

...
```
2.
```
Prediction: =
Function:
def get_head(repo_path):
    """Get (branch, commit) from HEAD of a git repo."""
    try:
        ref = open(os.path.join(repo_path, '.git', 'HEAD'), 'r').read().strip()[5:].split('/')
        branch = ref[-1]
        commit = open(os.path.join(repo_path, '.git', *ref), 'r').read().strip()[:7]
        return branch, commit
    except:
        return None

Prediction: }
Function:
def warn_for_shell_commands(command)
      case command
      when /^cp /i
        log.warn(log_key) { "Detected command `cp'. Consider using the `copy' DSL method." }
      when /^rubocopy /i
        log.warn(log_key) { "Detected command `rubocopy'. Consider using the `sync' DSL method." }
      when /^mv /i
        log.warn(log_key) { "Detected command `mv'. Consider using the `move' DSL method." }
      when /^rm /i
        log.warn(log_key) { "Detected command `rm'. Consider using the `delete' DSL method." }
      when /^remove /i
        log.warn(log_key) { "Detected command `remove'. Consider using the `delete' DSL method." }
      when /^rsync /i
        log.warn(log_key) { "Detected command `rsync'. Consider using the `sync' DSL method." }
      when /^strip /i
        log.warn(log_key) { "Detected command `strip'. Consider using the `strip' DSL method." }
      end
    end
```

Второй пример на Ruby, есть предположение, что происходит из-за частого
вхождения символа `}`.

3.

```
Prediction: main
Function:
def task_state(args):
    """
    Returns the state of a TaskInstance at the command line.
    >>> airflow task_state tutorial sleep 2015-01-01
    success
    """
    dag = get_dag(args)
    task = dag.get_task(task_id=args.task_id)
    ti = TaskInstance(task, args.execution_date)
    print(ti.current_state())
```

== А иногда справляется (почти) лучше, чем разработчики

```
Prediction: upload
Function: 
def execute(self, context):
        """
        Uploads the file to Google cloud storage
        """
        hook = GoogleCloudStorageHook(
            google_cloud_storage_conn_id=self.google_cloud_storage_conn_id,
            delegate_to=self.delegate_to)

        hook.upload(
            bucket_name=self.bucket,
            object_name=self.dst,
            mime_type=self.mime_type,
            filename=self.src,
            gzip=self.gzip,
        )
```
