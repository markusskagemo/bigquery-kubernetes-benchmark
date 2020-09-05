### Cloud BigQuery benchmarking  
Kubernetes microservice som tar tider på read/write og andre tap av tid sett bort fra google slot time.  
Tanken er at denne kjører på en pod i Finland og testes opp mot BigQuery-"serveren" som også ligger i Finland.  
Benchmarks blir lagret i *times.csv*.  

#### Merk  
* Credential-filen, 'quantum-fusion-nnnnn.json' bør ikke oppbevares her i klartekst. I tilfellet må den defineres i .gitignore  
* Mangler requirement.txt, config.sh og andre org-ting som .yaml-filen for docker.  

```
pip3 install -r requirements.txt
```