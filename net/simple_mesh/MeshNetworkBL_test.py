#=========================================================================
# Mesh Unit Test
#=========================================================================

import random

from pymtl        import *
from pclib.ifaces import NetMsg
from pclib.test   import TestSource, TestNetSink

from MeshNetworkBL import MeshNetworkBL

import traffic_generators
from traffic_generators import *

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------
class TestHarness( Model ):

  #-----------------------------------------------------------------------
  # __init__
  #-----------------------------------------------------------------------
  def __init__( s, src_msgs, sink_msgs, src_delay, sink_delay,
                nrouters, nmessages, payload_nbits, nentries ):

    s.src_msgs      = src_msgs
    s.sink_msgs     = sink_msgs
    s.src_delay     = src_delay
    s.sink_delay    = sink_delay
    s.nrouters      = nrouters
    s.nmessages     = nmessages
    s.payload_nbits = payload_nbits
    s.nentries      = nentries

  #-----------------------------------------------------------------------
  # elaborate_logic
  #-----------------------------------------------------------------------
  def elaborate_logic( s ):

    # instantiate models

    msg_type = NetMsg( s.nrouters, s.nmessages, s.payload_nbits )

    s.src  = [ TestSource ( msg_type, s.src_msgs[x],  s.src_delay  ) for x in xrange( s.nrouters ) ]
    s.mesh = MeshNetworkBL( s.nrouters, s.nmessages, s.payload_nbits, s.nentries )
    s.sink = [ TestNetSink( msg_type, s.sink_msgs[x], s.sink_delay ) for x in xrange( s.nrouters ) ]

    # connect signals

    for i in xrange( s.nrouters ):
      s.connect( s.mesh.in_[i], s.src[i].out  )
      s.connect( s.mesh.out[i], s.sink[i].in_ )

  #-----------------------------------------------------------------------
  # done
  #-----------------------------------------------------------------------
  def done( s ):
    done_flag = 1
    for i in xrange( s.nrouters ):
      done_flag &= s.src[i].done and s.sink[i].done
    return done_flag

  #-----------------------------------------------------------------------
  # line_trace
  #-----------------------------------------------------------------------
  def line_trace( s ):
    return s.mesh.line_trace()

#-------------------------------------------------------------------------
# run_net_test
#-------------------------------------------------------------------------
# RunTest Utility Function
def run_net_test( dump_vcd, vcd_file_name, src_delay, sink_delay,
                  test_msgs, nrouters, nmessages, payload_nbits,
                  nentries ):

  # src/sink msgs

  src_msgs  = test_msgs[0]
  sink_msgs = test_msgs[1]

  # Instantiate and elaborate the model

  model = TestHarness( src_msgs, sink_msgs, src_delay, sink_delay,
                       nrouters, nmessages, payload_nbits, nentries )
  model.elaborate()

  # Create a simulator using the simulation tool

  sim = SimulationTool( model )
  if dump_vcd:
    sim.dump_vcd( vcd_file_name )

  # Run the simulation

  print ""

  sim.reset()
  while not model.done():
    sim.print_line_trace()
    sim.cycle()

  # Add a couple extra ticks so that the VCD dump is nicer

  sim.cycle()
  sim.cycle()
  sim.cycle()

#-------------------------------------------------------------------------
# network args
#-------------------------------------------------------------------------

nrouters      = traffic_generators.nrouters      =  16
nmessages     = traffic_generators.nmessages     = 128
payload_nbits = traffic_generators.payload_nbits =  32

nentries = 4

#-------------------------------------------------------------------------
# terminal tests
#-------------------------------------------------------------------------

def test_mesh_terminal_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_terminal_delay0x0.vcd", 0, 0,
                terminal_msgs(), nrouters, nmessages, payload_nbits,
                nentries )

def test_mesh_terminal_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_terminal_delay5x0.vcd", 5, 0,
                terminal_msgs(), nrouters, nmessages, payload_nbits,
                nentries )

def test_mesh_terminal_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_terminal_delay0x5.vcd", 0, 5,
                terminal_msgs(), nrouters, nmessages, payload_nbits,
                nentries )

def test_mesh_terminal_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_terminal_delay8x5.vcd", 8, 5,
                terminal_msgs(), nrouters, nmessages, payload_nbits,
                nentries )

#-------------------------------------------------------------------------
# nearest neighbor east tests
#-------------------------------------------------------------------------

def test_mesh_nearest_neighbor_east_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_east_delay0x0.vcd", 0, 0,
                nearest_neighbor_east_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

def test_mesh_nearest_neighbor_east_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_east_delay5x0.vcd", 5, 0,
                nearest_neighbor_east_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

def test_mesh_nearest_neighbor_east_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_east_delay0x5.vcd", 0, 5,
                nearest_neighbor_east_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

def test_mesh_nearest_neighbor_east_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_east_delay8x5.vcd", 8, 5,
                nearest_neighbor_east_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

#-------------------------------------------------------------------------
# nearest neighbor west tests
#-------------------------------------------------------------------------

def test_mesh_nearest_neighbor_west_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_west_delay0x0.vcd", 0, 0,
                nearest_neighbor_west_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )


def test_mesh_nearest_neighbor_west_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_west_delay5x0.vcd", 5, 0,
                nearest_neighbor_west_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

def test_mesh_nearest_neighbor_west_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_west_delay0x5.vcd", 0, 5,
                nearest_neighbor_west_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

def test_mesh_nearest_neighbor_west_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_nearest_neighbor_west_delay8x5.vcd", 8, 5,
                nearest_neighbor_west_msgs(8), nrouters,
                nmessages, payload_nbits, nentries )

#-------------------------------------------------------------------------
# hotspot tests
#-------------------------------------------------------------------------

def test_mesh_hotspot_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_hotspot_delay0x0.vcd", 0, 0,
                hotspot_msgs(3), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_hotspot_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_hotspot_delay5x0.vcd", 5, 0,
                hotspot_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_hotspot_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_hotspot_delay0x5.vcd", 0, 5,
                hotspot_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_hotspot_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_hotspot_delay8x5.vcd", 8, 5,
                hotspot_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

#-------------------------------------------------------------------------
# partition tests
#-------------------------------------------------------------------------

def test_mesh_partition_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_partition_delay0x0.vcd", 0, 0,
                partition_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_partition_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_partition_delay5x0.vcd", 5, 0,
                partition_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_partition_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_partition_delay0x5.vcd", 0, 5,
                partition_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_partition_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_partition_delay8x5.vcd", 8, 5,
                partition_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

#-------------------------------------------------------------------------
# uniform random tests
#-------------------------------------------------------------------------

def test_mesh_uniform_random_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_uniform_random_delay0x0.vcd", 0, 0,
                uniform_random_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_uniform_random_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_uniform_random_delay0x5.vcd", 0, 5,
                uniform_random_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_uniform_random_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_uniform_random_delay5x0.vcd", 5, 0,
                uniform_random_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_uniform_random_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_uniform_random_delay8x5.vcd", 8, 5,
                uniform_random_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

#-------------------------------------------------------------------------
# tornado tests
#-------------------------------------------------------------------------

def test_mesh_tornado_delay0x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_tornado_delay0x0.vcd", 0, 0,
                tornado_msgs(24), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_tornado_delay5x0( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_tornado_delay5x0.vcd", 5, 0,
                tornado_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_tornado_delay0x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_tornado_delay0x5.vcd", 0, 5,
                tornado_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

def test_mesh_tornado_delay8x5( dump_vcd ):
  run_net_test( dump_vcd, "Mesh_tornado_delay8x5.vcd", 8, 5,
                tornado_msgs(8), nrouters, nmessages,
                payload_nbits, nentries )

