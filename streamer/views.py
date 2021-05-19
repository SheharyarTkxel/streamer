from django.shortcuts import render
import os
import re
import datetime
from .settings import MEDIA_ROOT


def reset_zero(ms):

    """

    :param ms:
    :return: It takes milliseconds as a parameter and checks if it is zero or not.
    If it is zero then it appends three 0's at the end of parameter and return the output in three digits.
    """

    ms = str(int(ms))
    while len(ms) < 3:
        ms += "0"
    return ms


def offset_time(offset, time_string):

    """

    :param offset:
    :param time_string:
    :return: It converts offset which is entered by the user to it's equivalent seconds and milliseconds and then
    returns timestamp in the format similar to SRT file's format.
    """

    ts = time_string.replace(',', ':').split(':')
    ts = [int(x) for x in ts]
    ts = datetime.datetime(2013, 1, 1, ts[0], ts[1], ts[2], ts[3] * 1000)
    delta = datetime.timedelta(seconds=offset)
    ts += delta

    if ts.year != 2013 or ts.month != 1 or ts.day != 1:
        return False

    return "%s,%s" % (ts.strftime("%H:%M:%S"), reset_zero(ts.microsecond / 1000))


def streamer_tool(request):

    """

    :param request:
    :return: It calls offset_time() function which further calls reset_zero() function for the SRT file modification.
     After that it writes data into new file and removes the uploaded file and returns an appropriate response to the
     user.
    """

    flag = False

    if request.method == 'POST':
        srt = request.FILES['file']
        file_name = srt.name
        offset = float(request.POST.get('offset'))

        with open(MEDIA_ROOT + "/" + file_name, 'wb+') as f:
            for chunk in srt.chunks():
                f.write(chunk)

        updated_file_name = '(Processed)' + ' ' + file_name

        out_filename = os.path.join(MEDIA_ROOT, updated_file_name)

        with open(out_filename, 'w', encoding='utf-8') as out:
            with open(MEDIA_ROOT + "/" + file_name, 'r', encoding='utf-8') as srt:
                for line in srt.readlines():
                    match = re.search(r'^(\d+:\d+:\d+,\d+)\s+-->\s+(\d+:\d+:\d+,\d+)', line)
                    if match:
                        if offset_time(offset, match.group(1)) is False:
                            return render(request, 'streamer.html',
                                          {'msg': 'Invalid offset resulting timestamp overflow'})

                        out.write("%s --> %s\n" % (
                            offset_time(offset, match.group(1)),
                            offset_time(offset, match.group(2))
                        ))
                    else:
                        out.write(line)
        flag = True
        os.remove(MEDIA_ROOT + "/" + file_name)
        return render(request, 'streamer.html',
                      {'flag': flag,
                       'fileName': updated_file_name,
                       'second_msg': 'File processed successfully. Please click Save As button to download it'})

    return render(request, 'streamer.html', {'flag': flag})
