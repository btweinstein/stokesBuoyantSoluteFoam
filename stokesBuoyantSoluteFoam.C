/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011-2016 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    simpleFoam

Description
    Steady-state solver for incompressible, turbulent flow, using the SIMPLE
    algorithm.

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "singlePhaseTransportModel.H"
#include "turbulentTransportModel.H"
#include "simpleControl.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "postProcess.H"

    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"
    #include "createControl.H"
    #include "createTimeControls.H"
    #include "createFields.H"
    #include "initContinuityErrs.H"
  
    while (runTime.run())
    {
        #include "readTimeControls.H"
        #include "CourantNo.H"
        #include "setDeltaT.H"

        runTime++;

        Info<< "Time = " << runTime.timeName() << nl << endl;

        //*** Calculate the concentration field ***

        while (simple.correctNonOrthogonal())
        {
            fvScalarMatrix cEqn
            (
                fvm::ddt(c)
              + fvm::div(phi, c)
              - fvm::laplacian(D_star, c)
            );
            cEqn.solve();
        }

        //*** Calculate the velocity field***

        double U_res_init = 1;
        double P_res_init = 1;
	
    	volScalarField rhok("rhok", Ra*c); // For consistent notation with bousinesq

        int stokes_iter = 0;

	    // Conditions to continue looping
	    bool gt_res = true; // Greater than residual cutoffs
	    bool lt_max_iter = true; // Less than maximum iteration
	    bool lt_min_iter = true; // Less than minimum iteration
		
        while((gt_res && lt_max_iter) || lt_min_iter)
        {
            p_rgh.storePrevIter();

            // --- Pressure-velocity SIMPLE corrector
            {
                #include "UEqn.H"
                #include "pEqn.H"
            }

            laminarTransport.correct();
            turbulence->correct();

            Info << "Finished stokes iteration " << stokes_iter << nl << endl;

            stokes_iter++;

            // Recalculate the termination conditions
            gt_res = (U_res_init > U_converged) || (P_res_init > p_converged);
            lt_max_iter = (stokes_iter <= max_stokes_iter);
            lt_min_iter = (stokes_iter <= min_stokes_iter);
        }
        
        if(!lt_max_iter) // i.e. ran out of iterations
        {
	        Info<< "Ran for maximum number of stokes iterations." << endl;
	    }
	    Info<< "Stokes solver converged in " << stokes_iter - 1 << " iterations." << nl << endl;

        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;	
    }

    Info<< "End\n" << endl;
    
    return 0;
}


// ************************************************************************* //
