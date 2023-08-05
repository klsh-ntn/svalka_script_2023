#!/usr/bin/env python
# -*- coding: utf-8 -*-

# $URL: svn+ssh://svnuser@klsh.org/home/svnuser/klsh_2011/fmt/scripts/final_ordered_list $
# $Id: final_ordered_list 7 2011-07-21 09:02:25Z dennis $
import schedule

#################################################################
#### Define team rank as number of teams with smaller score: ####
#################################################################

def rankmap(scoremap):
    result = {}

    for k in scoremap.keys():
        result[k] = 0

        for ok in scoremap.keys():
            if k != ok and scoremap[k] > scoremap[ ok ]:
                result[k] = result[k] + 1

    print("rankmap: ", result)
    return result



##########################
#### Main Tournament: ####
##########################

scoremap_main = {}
scoremap_main[r'$\chi$'] = 12
scoremap_main[r'$\delta$'] = 17
scoremap_main[r'$\tau$'] = 6
scoremap_main[r'$\alpha$'] = 22
scoremap_main[r'$\beta$'] = 15
scoremap_main[r'$o$'] = 5
scoremap_main[r'$\rho$'] = 7
scoremap_main[r'$\nu$'] = 14
scoremap_main[r'$\theta$'] = 9
scoremap_main[r'$\iota$'] = 10
scoremap_main[r'$\eta$'] = 23
scoremap_main[r'$\varphi$'] = 16
scoremap_main[r'$\gamma$'] = 20
scoremap_main[r'$\kappa$'] = 19
scoremap_main[r'$\lambda$'] = 8
scoremap_main[r'$\upsilon$'] = 18
scoremap_main[r'$\xi$'] = 4
scoremap_main[r'$\mu$'] = 1
scoremap_main[r'$\pi$'] = 21
scoremap_main[r'$\sigma$'] = 0
scoremap_main[r'$\omega$'] = 11
scoremap_main[r'$\varepsilon$'] = 2
scoremap_main[r'$\psi$'] = 3
scoremap_main[r'$\zeta$'] = 13

#################
#### Свалка: ####
#################

team_times = {}
team_scores = {}
for team in schedule.svalka:
    team_scores[team['TEAM']] = team['SCORES']
    team_times[team['TEAM']] = 0

    for p in range(4):
        if team[ 'SCORES' ][p][0] == None:
            team_times[team['TEAM']] -= 20 * 60  # if the problem has to answer yet, we set maximum time in seconds
        else:
            if team[ 'SCORES' ][p][1] == 2:
                team_times[team['TEAM']] -= team['SCORES'][p][0] / 2.0  # schedule.svalka keeps scores in secs
            elif team[ 'SCORES' ][p][1] == 1:
                team_times[team['TEAM']] -= team['SCORES'][p][0]
            elif team[ 'SCORES' ][p][1] == 3:
                team_times[team['TEAM']] -= team['SCORES'][p][0] / 3.0
            else:
                team_times[team['TEAM']] -= 20 * 60  # 0 points = full time

scoremap_svalka = rankmap(team_times)
print('!!!', scoremap_svalka)
####################
#### Team Rank: ####
####################

class TeamRank:
    def __lt__( self, other ):
        srank = self.mainrank + self.svalkarank
        orank = other.mainrank + other.svalkarank
        if srank != orank:
            return srank < orank
        return self.mainrank < other.mainrank

    def __repr__( self ):
        return '%s: основной тур -- %d, свалка -- %d, общий -- %d' % ( schedule.latex2greek[ self.team ],
                                                                       self.mainrank,
                                                                       self.svalkarank,
                                                                       self.mainrank + self.svalkarank )

##########################
#### Final Rank List: ####
##########################

ranklist = []

for k in scoremap_main.keys():
    tr = TeamRank()
    tr.mainrank = scoremap_main[k]
    tr.svalkarank = scoremap_svalka[k]
    tr.team = k
    ranklist.append( tr )

ranklist.sort()
ranklist.reverse()

for tr in ranklist:
    print(tr)

######################
#### HTML Output: ####
######################

html_out = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru" dir="ltr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="refresh" content="1">
  </head>
  <body>
'''

html_out = html_out + '<p align="center"><table><tr>\n'
html_out = html_out + '<td><img src="klshlogo.png" '
html_out = html_out + 'height="300" width="300" alt="логотип КЛШ" /></td>\n'

html_out = html_out + '<td><table>\n'
html_out = html_out + '<tr align="center"><td><h1><font color="#0066FF">КРАСНОЯРСКАЯ ЛЕТНЯЯ ШКОЛА</font></h1></td></tr>\n'
html_out = html_out + '<tr align="center"><td><h2><font color="#0066FF">2023 год (46 сезон)</font></h2></td></tr>\n'
html_out = html_out + '</table></td>\n'

html_out = html_out + '</tr></table></p>\n'

html_out = html_out + '<p><h1 align="center"><font color="#0066FF">Текущие результаты физико-математического турнира</font></h1></p>\n'

html_out = html_out + '<br />\n<p align="center"><font size="+2"><table cellpadding="5" cellspacing="5">'
html_out = html_out + '<tr align="center">'
html_out = html_out + '<th>Команда:</th>'
html_out = html_out + '<th>Рейтинг в основном туре:</th>'
html_out = html_out + '<th>Задача 1:</th>'
html_out = html_out + '<th>Задача 2:</th>'
html_out = html_out + '<th>Задача 3:</th>'
html_out = html_out + '<th>Задача 4:</th>'
html_out = html_out + '<th>Полное время:</th>'
html_out = html_out + '<th>Текущий рейтинг в свалке:</th>'
html_out = html_out + '<th>Общий рейтинг:</th></tr>\n'

for tr in ranklist:
    html_out = html_out + '<tr align="center">'
    html_out = html_out + '<td>' + schedule.latex2greek[ tr.team ] + '</td>'
    html_out = html_out + ( '<td>%d</td>' % tr.mainrank )
    scores = team_scores[tr.team]
    total_time = 0
    for p in range(4):
        res = ' '
        if scores[p][0] is None:
            res = '<font color="#808000">1200</font>'
            total_time += 1200
        elif scores[p][1] == 0:
            res = '<font color="#008000"><b>1200</b></font>'
            total_time += 1200
        elif scores[p][1] == 1:
            res = '<font color="#00C000"><b>' + str(int(scores[p][0])) + '</b></font>'
            total_time += int(scores[p][0])
        elif scores[p][1] == 2:
            res = '<font color="#FF0000"><b>' + str(int(scores[p][0] // 2)) + '</b></font>'
            total_time += int(scores[p][0] // 2)
        elif scores[p][1] == 3:
            res = '<font color="#FF0000"><b>' + str(int(scores[p][0] // 3)) + '</b></font>'
            total_time += int(scores[p][0] // 2)
        html_out = html_out + '<td>' + res + '</td>'
    html_out = html_out + ( '<td>%d</td>' % total_time )
    html_out = html_out + ( '<td>%d</td>' % tr.svalkarank )
    html_out = html_out + ( '<td>%d</td>' % ( tr.mainrank + tr.svalkarank ) )
    html_out = html_out + '</tr>\n'

html_out = html_out + '</table></font></p>\n'

html_out = html_out + '''
  </body>
</html>
'''

html_out_f = open( 'results_after_svalka.html', 'w' )
html_out_f.write( html_out )
html_out_f.close()

#######################
#### LaTeX Output: ####
#######################

out = r'''% This is a generated file, do not edit
\documentclass[12pt]{article}
\usepackage[a4paper,top=1cm,bottom=1cm]{geometry}

\usepackage{graphicx}
\usepackage{color}

\usepackage[utf8]{inputenc}
\usepackage[T2A]{fontenc}
\usepackage[russian]{babel}

\begin{document}

\pagestyle{empty}

\begin{center}
\begin{tabular}{cc}
\includegraphics[scale=0.48]{klshlogo.pdf} &
\raisebox{0.5cm}{
  \begin{tabular}{c}
    {\Large\bf КРАСНОЯРСКАЯ ЛЕТНЯЯ ШКОЛА}\\
    \ \\
    {\large\bf Сезон 2022 года}\\
   \end{tabular}
}
\end{tabular}
\ \\
\ \\
\ \\
{\Large\bf Результаты физико--математического турнира}
\ \\
\end{center}

Команды расположены в таблице в порядке убывания итогового рейтинга. 
{\em Рейтингом} команды называется количество команд, выступивших
менее успешно. Итоговый рейтинг есть сумма рейтингов в основном туре и
свалке. В случае, когда две команды имеют одинаковую сумму рейтингов в
основном туре и свалке, более успешной считается команда, чей рейтинг
в основном туре выше.

Команды, занимающие \textcolor{red}{первое и второе место} в итоговом
рейтинге, встречаются в суперфинале за абсолютное первое
место. Команды, занимающие \textcolor{green}{третье и четвёртое
место}, встречаются за абсолютное третье место.

\vspace*{1cm}

\begin{center}
    \begin{tabular}{|c|c|c|c|}

      \hline
      {\bf Команда} & {\bf Основной тур} &
      {\bf Финальная свалка} & {\bf Итоговый рейтинг} \\

      \hline
      \hline
'''

place = 0
for tr in ranklist:
    color = 'black'
    if place < 2:
        color = 'red'
    elif place < 4:
        color = 'green'
    out = out + r'\textcolor{' + color + r'}{' + tr.team + r'} & ' + '\n'
    out = out + r'\textcolor{' + color + r'}{' + ( '%d' % tr.mainrank ) + r'} & ' + '\n'
    out = out + r'\textcolor{' + color + r'}{' + ( '%d' % tr.svalkarank ) + r'} & ' + '\n'
    out = out + r'\textcolor{' + color + r'}{' + ( '%d' % ( tr.mainrank + tr.svalkarank ) )
    out = out + r'} \\ ' + '\n'
    out = out + r'\hline' + '\n'
    place = place + 1

out = out + r'\hline' + '\n'

out = out + r'''
    \end{tabular}

  \end{center}

\end{document}
'''

out_f = open( 'results_after_svalka.tex', 'w' )
out_f.write( out )
out_f.close()
