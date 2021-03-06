import os
import sys
import time

from datetime import datetime

import core
import grokpy


class ErcotStreamSpec(grokpy.StreamSpecification):
  def __init__(self, name):
    super(ErcotStreamSpec, self).__init__()

    self.setName(name)

    # Create a Data Source and specify fields
    local = grokpy.LocalDataSource()
    local.setName(name)

    # Create each of our fields
    timestamp = grokpy.DataSourceField()
    timestamp.setName('timestamp')
    timestamp.setType(grokpy.DataType.DATETIME)
    timestamp.setFlag(grokpy.DataFlag.TIMESTAMP)

    demand = grokpy.DataSourceField()
    demand.setName('demand')
    demand.setType(grokpy.DataType.SCALAR)

    # Add our fields to our source
    local.addField(timestamp)
    local.addField(demand)

    # Add our source to the stream specification
    self.addDataSource(local)


  @staticmethod
  def formatRecord(record):
    return [
      str(datetime.strptime(
        record.DeliveryDate + ' ' + record.TimeEnding, '%m/%d/%Y %H:%M')),
      record.Demand
    ]


class ErcotModelSpec(grokpy.ModelSpecification):
  def __init__(self, name, stream,
      predictedField='demand',
      predictionSteps=None):

    super(ErcotModelSpec, self).__init__()

    self.setName(name)
    self.setPredictedField('demand')
    self.setStream(stream.id)

    if predictionSteps is not None:
      self.setPredictionSteps(predictionSteps)


def system_wide_demand():
  """ Main entry point. """

  cli = core.getCLIParser()

  (options, args) = cli.parse_args()
  try:
    target = args.pop(0)
  except IndexError:
    cli.print_help()
    return

  name = target + ' ' + datetime.now().isoformat().partition('.')[0]

  """ Grok client """
  try:
    grok = grokpy.Client(key=options.apiKey, baseURL=options.apiUrl)
  except grokpy.exceptions.AuthenticationError:
    if options.apiKey is not None or 'GROK_API_KEY' in os.environ:
      print "ERROR: Invalid API Key (", \
        (options.apiKey or os.environ['GROK_API_KEY']), ")"
    elif 'GROK_API_KEY' not in os.environ:
      print "ERROR: Perhaps you did not specify an API Key?\n"

    cli.print_help()
    return

  """ Create project """
  project = grok.createProject(name)

  print project.name, 'project created (', project.id, ')'

  """ Create stream """
  streamSpec = ErcotStreamSpec(name)
  ercotStream = project.createStream(streamSpec)

  print ercotStream.name, 'stream created (', ercotStream.id, ')'

  """ Populate stream with historical training data """

  print 'Appending historical data to stream...',

  ercotStream.addRecords(map(ErcotStreamSpec.formatRecord,
    sorted(core.collect(target))))

  print 'Done.'

  """ Base model """
  ercotModel = project.createModel(ErcotModelSpec(name, ercotStream))
  print ercotModel.name, 'model created (', ercotModel.id, ')'

  """ Hour-ahead model """
  hourSpec = ErcotModelSpec(name + ' +1hr', ercotStream, predictionSteps=[4])
  ercotHourModel = project.createModel(hourSpec)
  print ercotHourModel.name, 'model created (', ercotHourModel.id, ')'

  """ Day-ahead model """
  daySpec = ErcotModelSpec(name + ' +24hrs', ercotStream, predictionSteps=[96])
  ercotDayModel = project.createModel(daySpec)
  print ercotDayModel.name, 'model created (', ercotDayModel.id, ')'

  models = (ercotModel, ercotHourModel, ercotDayModel)

  """ Start swarms """

  for model in models:
    model.startSwarm()

  """ Monitor swarms """
  pending = set(models)
  print "Swarming",
  while pending:
    completed = set()
    for model in pending:
      if ercotModel.getSwarmState()['status'] == grokpy.SwarmStatus.COMPLETED:
        completed.add(model)

    for model in completed:
        pending.remove(model)
    print ".",
    sys.stdout.flush()
    time.sleep(5)

  print "Done!"

  """ Print results """

  width = max(len(model.name) for model in models)

  print '\nModel' + ' ' * (width-4) + '| Error'
  print '-' * (width+1) + '|' + '-' * 17

  for model in models:
    state = model.getSwarmState()
    print ('{:<' + str(width) + '}').format(model.name), '|', \
      state['results']['averageError']


if __name__ == '__main__':
  system_wide_demand()
